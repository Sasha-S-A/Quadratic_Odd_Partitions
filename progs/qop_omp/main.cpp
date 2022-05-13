#include <stdio.h>
#include <math.h>
#include <memory.h>
#include <stdlib.h>
#include <omp.h>
#include <stdint.h>
#include <windows.h>

#define MOD4_MAX_LEN	64
#define MAX_NUMBERS		1000
#define MAX_PRIMES		168

typedef struct
{
	uint32_t n;
	uint32_t set_len;
	uint32_t set_len_minus_one;
	uint16_t buffer[MOD4_MAX_LEN][MOD4_MAX_LEN + 8];

	uint64_t qop;
}param_t;

uint32_t g_primes[MAX_PRIMES];
uint8_t g_decompos[MAX_NUMBERS][(MAX_PRIMES + 31) >> 3];

static void gen_primes(void)
{
	uint32_t i, j, k, nums[MAX_NUMBERS];

	for (i = 0; i < MAX_NUMBERS; i++)
		nums[i] = i;

	for (k = 0, i = 2; i < MAX_NUMBERS; i++)
	{
		if (nums[i] == 0)
			continue;

		g_primes[k++] = nums[i];
		for (j = i * i; j < MAX_NUMBERS; j += i)
			nums[j] = 0;
	}
}

static void gen_decompos(void)
{
	uint8_t* bitset;
	uint32_t i, j, tmp;

	for (i = 2; i < MAX_NUMBERS; i++)
	{
		for (tmp = i, j = 0; j < MAX_PRIMES; j++)
		{
			while (tmp % g_primes[j] == 0)
			{
				bitset = &g_decompos[i][j >> 3];
				if (*bitset & (1 << (j & 7)))
					*bitset &= ~(1 << (j & 7));
				else
					*bitset |= (1 << (j & 7));
				tmp /= g_primes[j];
			}
		}
	}
}

static uint32_t qop_levels_count(uint32_t n, uint32_t set_len)
{
	uint32_t levels, sum, i;

	levels = sum = 0;
	for (i = 0; i < set_len; i++)
		sum += 1 + (i << 1);

	while (1)
	{
		if (sum > n)
			return levels;
		else if (sum == n)
			return ++levels;
		else
		{
			levels++;
			sum += (set_len << 1);
		}
	}
}

static uint32_t qop_set_len_fill(uint32_t n, uint32_t* lens)
{
	uint32_t elemnum, eq, i, count;

	elemnum = (uint32_t)sqrt((float)n);
	if (elemnum > MOD4_MAX_LEN)
		elemnum = MOD4_MAX_LEN;

	eq = n % 4;
	count = 0;
	for (i = 1; i <= elemnum; i++)
	{
		if (eq == (i % 4))
			lens[count++] = i;
	}

	return count;
}

static void qop_lookup_r(uint32_t step, uint32_t sum, param_t* param)
{
	while (1)
	{
		if (sum < param->n)
		{
			if (param->set_len_minus_one ^ step)
			{
				uint16_t* cur;
				uint64_t* src, * dst;

				dst = (uint64_t*)param->buffer[step];
				src = (uint64_t*)param->buffer[step - 1];
				while (*src) *dst++ = *src++;

				qop_lookup_r(step + 1, sum, param);
				sum += (param->set_len - step) << 1;

				cur = &param->buffer[step - 1][step];
				while (*cur) *cur++ += 2;
			}
			else
			{
				param->buffer[step - 1][param->set_len_minus_one] += param->n - sum;
				sum = param->n;
			}
		}
		else if (!(sum ^ param->n))
		{
			uint16_t* cur;
			uint64_t* dec;
			uint64_t factors[3] = { 0 };

			cur = param->buffer[step - 1];
			while (*cur)
			{
				dec = (uint64_t*)g_decompos[*cur++];
				factors[0] = factors[0] ^ dec[0];
				factors[1] = factors[1] ^ dec[1];
				factors[2] = factors[2] ^ dec[2];
			}

			if (factors[0] || factors[1] || factors[2])
				return;

			param->qop++;
			return;
		}
		else
			return;
	}
}

static uint64_t qop_lookup(uint32_t i, uint32_t n, uint32_t set_len)
{
	uint32_t m, sum;
	param_t param = { 0 };

	param.n = n;
	param.set_len = set_len;
	param.set_len_minus_one = param.set_len - 1;

	sum = 0;
	for (m = 0; m < param.set_len; m++)
	{
		param.buffer[0][m] = (1 + (i << 1)) + (m << 1);
		sum += param.buffer[0][m];
	}

	qop_lookup_r(1, sum, &param);
	return param.qop;
}

static uint64_t qop_process_len(uint32_t n, uint32_t set_len)
{
	int i;
	uint64_t qop;
	uint32_t num_levels;

	if (set_len == 1)
	{
		if (n % 2 != 0)
		{
			double a = sqrt((double)n);
			if (a == (uint64_t)a)
				return 1;
		}
		return 0;
	}

	qop = 0;
	num_levels = qop_levels_count(n, set_len);

	#pragma omp parallel for num_threads(2) schedule(dynamic, 1) reduction(+:qop)
	for (i = 0; i < num_levels; i++)
		qop += qop_lookup(i, n, set_len);

	return qop;
}

static void qop_process_number(uint32_t n)
{
	int i;
	uint64_t qop, start;
	uint32_t lens[MOD4_MAX_LEN], count;

	qop = 0;
	count = qop_set_len_fill(n, lens);
	start = timeGetTime();

	#pragma omp parallel for num_threads(2) schedule(dynamic, 1) reduction(+:qop)
	for (i = count - 1; i >= 0; i--)
		qop += qop_process_len(n, lens[i]);

	printf("%d %.3f %llu\n", n, (float)(timeGetTime() - start) / 1000, qop);
}

int main(int argc, char* argv[])
{
	uint32_t n;

	gen_primes();
	gen_decompos();

	omp_set_nested(1);
	for (n = 1; n <= MAX_NUMBERS; n += 1)
		qop_process_number(n);

	return 0;
}