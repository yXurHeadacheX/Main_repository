def productExceptSelf(nums: list[int]) -> list[int]:
    output = [1] * len(nums)

    left = 1
    for i in range(len(nums)):
        output[i] *= left
        left *= nums[i]
        print("1:", output)
        print(left)

    right = 1
    for i in range(len(nums) - 1, -1, -1):
        output[i] *= right
        right *= nums[i]
        print("2:", output)
        print(right)

    return output

print(productExceptSelf([1,2,3,4]))
