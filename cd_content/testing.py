import test_generators as gen
import preprocesor as pre
import tests

SIZE = 12 * 8 * 1024 * 1024
TESTS = [
    ("overlapping_template_test",
     lambda vec: tests.overlapping_template_test(vec, [1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1])),

    ("frequency_test", lambda vec: tests.frequency_test(vec)),
    ("block_frequency_test_128", lambda vec: tests.block_frequency_test(vec, 128)),
    ("block_frequency_test_1024*", lambda vec: tests.block_frequency_test_1024(vec)),
    ("run_test", lambda vec: tests.run_test(vec)),
    ("longest_run_in_block_64", lambda vec: tests.longest_run_in_block_test(vec, 64, 1)),
    ("longest_run_in_block_1024*", lambda vec: tests.longest_run_in_block_test_1024(vec)),
    ("fourier_test", lambda vec: tests.fourier_test(vec)),

    ("linear_complexity_test", lambda vec: tests.linear_complexity_test(vec)),
    ("last_cross_test", lambda vec: tests.last_cross_test(vec)),
    ("max_cumsum_test", lambda vec: tests.max_cumsum_test(vec)),
    ("matrix_rank_test_32", lambda vec: tests.matrix_rank_test(vec, 32)),
    ("matrix_rank_test_16", lambda vec: tests.matrix_rank_test(vec, 16)),
]

SEED = 316545342

if __name__ == "__main__":
    data_my = pre.get_vector_from_ping("ping.txt")[0:SIZE]
    data_lcm = pre.convert_to_bit_vector(pre.load_from_file("prepared_num/lcm.txt"), 32)[0:SIZE]
    data_tarus = pre.convert_to_bit_vector(pre.load_from_file("prepared_num/tarus.txt"), 32)[0:SIZE]
    data_crng = pre.convert_to_bit_vector(pre.load_from_file("prepared_num/crng.txt"), 32)[0:SIZE]
    print("name;lcm;tarus;crng;my")
    for (name, t) in TESTS:
        p_lcm = t(data_lcm)
        p_tarus = t(data_tarus)
        p_crng = t(data_crng)
        p_my = t(data_my)
        print(name + ";" + str(p_lcm) + ";" + str(p_tarus) + ";" + str(p_crng) + ";" + str(p_my))
