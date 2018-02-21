import unittest


class FSet:
    @staticmethod
    def a_set(elem):
        return True

    @staticmethod
    def contains(f, elem):
        return f(elem)

    @staticmethod
    def add_element(some_set, element):
        return FSet.union(some_set, FSet.singleton_set(element))

    @staticmethod
    def singleton_set(elem):
        return lambda x: elem == x

    @staticmethod
    def union(set1, set2):
        return lambda x: FSet.contains(set1, x) or FSet.contains(set2, x)

    @staticmethod
    def intersect(set1, set2):
        return lambda x: FSet.contains(set1, x) and FSet.contains(set2, x)

    @staticmethod
    def diff(set1, set2):
        return lambda x: FSet.contains(set1, x) and not FSet.contains(set2, x)

    @staticmethod
    def filter(set1, condition):
        return lambda x: False if condition(x) is False else FSet.contains(set1, x)


class FSetTest(unittest.TestCase):
    def test_contains_is_implemented(self):
        self.assertTrue(FSet.contains(FSet.a_set, 100))

    def test_singleton_set_contains_one_element(self):
        self.assertTrue(FSet.contains(FSet.singleton_set(1), 1))

    def test_union_contains_all_elements(self):
        some_set = FSet.singleton_set(1)
        some_set = FSet.add_element(some_set, 2)
        self.assertTrue(FSet.contains(some_set, 1))
        self.assertTrue(FSet.contains(some_set, 2))
        self.assertFalse(FSet.contains(some_set, 3))

    def test_intersect_contains_a_shared_value(self):
        union1 = FSet.union(FSet.singleton_set(1), FSet.singleton_set(2))
        union2 = FSet.union(FSet.singleton_set(2), FSet.singleton_set(3))
        intersect_set = FSet.intersect(union1, union2)
        self.assertTrue(FSet.contains(intersect_set, 2))
        self.assertFalse(FSet.contains(intersect_set, 1))
        self.assertFalse(FSet.contains(intersect_set, 3))

    def test_diff_contains_elements_from_set1_which_are_not_present_in_set2(self):
        union1 = FSet.union(FSet.singleton_set(1), FSet.singleton_set(2))
        union2 = FSet.union(FSet.singleton_set(2), FSet.singleton_set(3))
        diff_set = FSet.diff(union1, union2)
        self.assertTrue(FSet.contains(diff_set, 1))
        self.assertFalse(FSet.contains(diff_set, 2))
        self.assertFalse(FSet.contains(diff_set, 3))

    def test_filter_contains_elements_that_match_the_criteria(self):
        set1 = FSet.union(FSet.singleton_set(1), FSet.singleton_set(2))
        union = FSet.union(set1, FSet.singleton_set(3))
        filtered_set = FSet.filter(union, lambda x: x > 1)
        self.assertTrue(FSet.contains(filtered_set, 3))
        self.assertTrue(FSet.contains(filtered_set, 2))
        self.assertFalse(FSet.contains(filtered_set, 1))
