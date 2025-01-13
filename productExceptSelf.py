def productExceptSelf(nums: list[int]) -> list[int]:
    output = [1] * len(nums)

    left = 1
    for i in range(len(nums)):
        output[i] *= left
        left *= nums[i]

    right = 1
    for i in range(len(nums) - 1, -1, -1):
        output[i] *= right
        right *= nums[i]

    return output

if __name__ == '__main__':
    print(productExceptSelf([1,2,3,4]))
