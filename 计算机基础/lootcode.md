[toc]

## 1.数组

## 1.1.移动零(283)

```python
给定一个数组 `nums`，编写一个函数将所有 `0` 移动到数组的末尾，同时保持非零元素的相对顺序。

'''
1.快慢指针：
定义两个指针，从头开始遍历，fast指针一直向后移，如果fast指针的值不为零，slow指针加一，并且把fast的值给slow，当fast的值超出序列下标，从slow所处位置开始补零

也可以直接把slow与fast的值进行交换
 
'''
```

## 1.2.移除元素

```python
给你一个数组 nums 和一个值 val，你需要 原地 移除所有数值等于 val 的元素，并返回移除后数组的新长度。

'''
简单解法1：
    直接判断目标值是否还在列表内，如果有直接删除，直到没有就行了

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        while val in nums:
            nums.remove(val)
        return len(nums)

解法2：
    使用双指针，如果快指针不等于目标值，则与慢指针交换值后两指针都进1，否则只有快指针进1，当快指针到列表尾后，返回慢指针的值
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        fast = slow =0
        while fast < len(nums):
            if nums[fast] != val:
                nums[slow] = nums[fast]
                slow += 1
            fast += 1
        return slow
'''
```

## 1.3.删除有序数组中的重复元素(80)

```python
给你一个有序数组 nums ，请你 原地 删除重复出现的元素，使得出现次数超过两次的元素只出现两次 ，返回删除后数组的新长度。

'''
1.双指针
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        slow = 1
        for fast in range(2,len(nums)):
            if nums[slow] == nums[fast] and nums[slow-1] == nums[fast]:
                continue
            slow += 1
            nums[slow] = nums[fast]
        return slow+1        
'''
```

## 1.4.颜色分类

```python
给定一个包含红色、白色和蓝色、共 n 个元素的数组 nums ，原地对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。

我们使用整数 0、 1 和 2 分别表示红色、白色和蓝色。
'''
1.三指针法
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # 创建两指针一头一尾，分别用来存放0和1
        p0 = i= 0
        p2 = len(nums)-1
        while i <= p2:
        	
            while i<=p2 and nums[i] == 2:
                nums[p2],nums[i] = nums[i],nums[p2]
                p2 -= 1
            if nums[i] == 0:
                nums[p0],nums[i] = nums[i],nums[p0]
                p0 += 1
            i += 1
'''
```

