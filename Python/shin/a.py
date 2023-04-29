def median(*nums):
    nums = list(nums)
    nums.sort()
    m_index = len(nums) // 2

    if len(nums) == 0:
        return None
    elif len(nums) % 2 == 0:
        return (nums[m_index - 1] + nums[m_index]) / 2
    else:
        return nums[m_index]


print('median(6, 3, 9):', median(6, 3, 9))
print('median(5, 4, 3, 2, 1, 0):', median(5, 4, 3, 2, 1, 0))