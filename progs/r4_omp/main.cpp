#include <stdio.h>
#include <math.h>
#include <memory.h>
#include <stdlib.h>
#include <stdint.h>
#include <omp.h>
#include <windows.h>

#define MOD4_MAX_LEN	64
#define MAX_NUMBERS		1000

typedef struct
{
	uint32_t n;
	uint32_t set_len;
	uint32_t set_len_minus_one;

	uint64_t r4;
}param_t;

static uint32_t r4_levels_count(uint32_t n, uint32_t set_len)
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

static uint32_t r4_set_len_fill(uint32_t n, uint32_t* lens)
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

static void r4_lookup_r(uint32_t step, uint32_t sum, param_t* param)
{
	while (1)
	{
		if (sum < param->n)
		{
			if (param->set_len_minus_one ^ step)
			{
				r4_lookup_r(step + 1, sum, param);
				sum += (param->set_len - step) << 1;
			}
			else
			{
				param->r4++;
				return;
			}
		}
		else if (!(sum ^ param->n))
		{
			param->r4++;
			return;
		}
		else
			return;
	}
}

static uint64_t r4_lookup(uint32_t i, uint32_t n, uint32_t set_len)
{
	uint32_t m, sum;
	param_t param;

	param.n = n;
	param.r4 = 0;
	param.set_len = set_len;
	param.set_len_minus_one = param.set_len - 1;

	sum = 0;
	for (m = 0; m < param.set_len; m++)
		sum += (1 + (i << 1)) + (m << 1);

	r4_lookup_r(1, sum, &param);
	return param.r4;
}

static uint64_t r4_process_len(uint32_t n, uint32_t set_len)
{
	int i;
	uint64_t r4;
	uint32_t num_levels;

	if (set_len == 1)
	{
		if (n % 2 != 0)
			return 1;
		return 0;
	}

	r4 = 0;
	num_levels = r4_levels_count(n, set_len);

	#pragma omp parallel for num_threads(2) schedule(dynamic, 1) reduction(+:r4)
	for (i = 0; i < num_levels; i++)
		r4 += r4_lookup(i, n, set_len);

	return r4;
}

static void r4_process_number(uint32_t n)
{
	int i;
	uint64_t r4, start;
	uint32_t lens[MOD4_MAX_LEN], count;

	r4 = 0;
	count = r4_set_len_fill(n, lens);
	start = timeGetTime();

	#pragma omp parallel for num_threads(2) schedule(dynamic, 1) reduction(+:r4)
	for (i = count - 1; i >= 0; i--)
		r4 += r4_process_len(n, lens[i]);

	printf("%d %.3f %llu\n", n, (float)(timeGetTime() - start) / 1000, r4);
}

int main(int argc, char* argv[])
{
	uint32_t n;

	omp_set_nested(1);
	for (n = 1; n <= MAX_NUMBERS; n += 1)
		r4_process_number(n);

	return 0;
}