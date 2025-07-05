#!/usr/bin/env python3
"""
Programming Challenges and Problem Solving Module

This module contains various algorithmic challenges that help develop
problem-solving skills and understanding of optimization techniques.
"""

def set_context(data_type):
    """Set the current context for cs() function based on data type."""
    global _current_context
    _current_context = data_type

def check_interactive_mode():
    """Placeholder function - will be replaced by main script's version"""
    pass

def step_through_function(func, global_ns=None, local_ns=None):
    """Placeholder function - will be replaced by main script's version"""
    func()

def snippet_section(code_lines, description=None):
    """Placeholder function - will be replaced by main script's version"""
    pass

def fibonacci_recursive(n):
    """Basic recursive Fibonacci - inefficient for large n."""
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

def fibonacci_memoized(n, memo=None):
    """Memoized Fibonacci - much more efficient."""
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memoized(n-1, memo) + fibonacci_memoized(n-2, memo)
    return memo[n]

def fibonacci_iterative(n):
    """Iterative Fibonacci - most efficient for this problem."""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def challenges_module(step=False):
    """
    Demonstrates various programming challenges and problem-solving techniques.
    Shows algorithms including memoization and dynamic programming patterns.
    If step=True, drops into interactive shell after every line in this block.
    """
    def challenges_block():
        set_context('challenges')
        
        print("🧩 Programming Challenges and Problem Solving")
        print("=" * 60)
        print("This module contains common algorithmic challenges that help develop")
        print("problem-solving skills and understanding of optimization techniques.")
        print("Each challenge includes multiple approaches and explanations.")
        print()
        
        check_interactive_mode()
    
    # Challenge 1: Fibonacci Numbers with Memoization
    print("🔢 Challenge 1: Fibonacci Numbers")
    print("-" * 30)
    print("Calculate Fibonacci numbers using different approaches")
    
    n = 10
    print(f"Calculating Fibonacci({n}):")
    
    # Show the basic recursive approach (inefficient)
    result_recursive = fibonacci_recursive(n)
    print(f"Recursive approach: {result_recursive}")
    
    # Show memoized approach (efficient)
    result_memoized = fibonacci_memoized(n)
    print(f"Memoized approach: {result_memoized}")
    
    # Show iterative approach (most efficient)
    result_iterative = fibonacci_iterative(n)
    print(f"Iterative approach: {result_iterative}")
    
    snippet_section([
        "# Fibonacci with memoization",
        "def fibonacci_memoized(n, memo=None):",
        "    if memo is None:",
        "        memo = {}",
        "    if n in memo:",
        "        return memo[n]",
        "    if n <= 1:",
        "        return n",
        "    memo[n] = fibonacci_memoized(n-1, memo) + fibonacci_memoized(n-2, memo)",
        "    return memo[n]",
        "",
        f"result = fibonacci_memoized({n})",
        f"print(f'Fibonacci({n}) = {{result}}')"
    ], "Fibonacci with memoization")
    
    check_interactive_mode()
    
    # Challenge 2: Two Sum Problem
    print("\n🎯 Challenge 2: Two Sum")
    print("-" * 30)
    print("Find two numbers in an array that add up to a target")
    
    nums = [2, 7, 11, 15]
    target = 9
    
    def two_sum(nums, target):
        """Find indices of two numbers that add up to target."""
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []
    
    result = two_sum(nums, target)
    print(f"Array: {nums}")
    print(f"Target: {target}")
    print(f"Indices: {result}")
    print(f"Values: [{nums[result[0]]}, {nums[result[1]]}]")
    
    snippet_section([
        "# Two Sum Problem",
        "def two_sum(nums, target):",
        "    seen = {}",
        "    for i, num in enumerate(nums):",
        "        complement = target - num",
        "        if complement in seen:",
        "            return [seen[complement], i]",
        "        seen[num] = i",
        "    return []",
        "",
        f"nums = {nums}",
        f"target = {target}",
        "result = two_sum(nums, target)",
        f"print(f'Indices: {{result}}')"
    ], "Two Sum with hash map")
    
    check_interactive_mode()
    
    # Challenge 3: Palindrome Check
    print("\n📝 Challenge 3: Palindrome Checker")
    print("-" * 30)
    print("Check if a string reads the same forwards and backwards")
    
    def is_palindrome(s):
        """Check if string is a palindrome (ignoring case and spaces)."""
        # Clean the string: remove non-alphanumeric and convert to lowercase
        cleaned = ''.join(char.lower() for char in s if char.isalnum())
        return cleaned == cleaned[::-1]
    
    test_strings = ["A man a plan a canal Panama", "race a car", "hello", "madam"]
    
    for test_str in test_strings:
        result = is_palindrome(test_str)
        print(f"'{test_str}' -> {result}")
    
    snippet_section([
        "# Palindrome Checker",
        "def is_palindrome(s):",
        "    cleaned = ''.join(char.lower() for char in s if char.isalnum())",
        "    return cleaned == cleaned[::-1]",
        "",
        "test_strings = ['A man a plan a canal Panama', 'race a car', 'madam']",
        "for test_str in test_strings:",
        "    result = is_palindrome(test_str)",
        "    print(f\"'{test_str}' -> {result}\")"
    ], "Palindrome checker")
    
    check_interactive_mode()
    
    # Challenge 4: Maximum Subarray Sum (Kadane's Algorithm)
    print("\n📊 Challenge 4: Maximum Subarray Sum")
    print("-" * 30)
    print("Find the contiguous subarray with the largest sum")
    
    def max_subarray_sum(nums):
        """Find maximum sum of contiguous subarray using Kadane's algorithm."""
        if not nums:
            return 0
        
        max_sum = current_sum = nums[0]
        
        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    test_array = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    result = max_subarray_sum(test_array)
    print(f"Array: {test_array}")
    print(f"Maximum subarray sum: {result}")
    
    snippet_section([
        "# Maximum Subarray Sum (Kadane's Algorithm)",
        "def max_subarray_sum(nums):",
        "    if not nums:",
        "        return 0",
        "    max_sum = current_sum = nums[0]",
        "    for num in nums[1:]:",
        "        current_sum = max(num, current_sum + num)",
        "        max_sum = max(max_sum, current_sum)",
        "    return max_sum",
        "",
        f"test_array = {test_array}",
        "result = max_subarray_sum(test_array)",
        f"print(f'Maximum sum: {{result}}')"
    ], "Kadane's algorithm")
    
    check_interactive_mode()
    
    # Challenge 5: Valid Parentheses
    print("\n🔗 Challenge 5: Valid Parentheses")
    print("-" * 30)
    print("Check if parentheses, brackets, and braces are balanced")
    
    def is_valid_parentheses(s):
        """Check if parentheses are properly balanced."""
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        
        for char in s:
            if char in mapping:
                if not stack or stack.pop() != mapping[char]:
                    return False
            else:
                stack.append(char)
        
        return not stack
    
    test_cases = ["()", "()[]{}", "(]", "([)]", "{[]}"]
    
    for test in test_cases:
        result = is_valid_parentheses(test)
        print(f"'{test}' -> {result}")
    
    snippet_section([
        "# Valid Parentheses Checker",
        "def is_valid_parentheses(s):",
        "    stack = []",
        "    mapping = {')': '(', '}': '{', ']': '['}",
        "    for char in s:",
        "        if char in mapping:",
        "            if not stack or stack.pop() != mapping[char]:",
        "                return False",
        "        else:",
        "            stack.append(char)",
        "    return not stack",
        "",
        "test_cases = ['()', '()[]{}}', '(]', '([)]', '{[]}']",
        "for test in test_cases:",
        "    result = is_valid_parentheses(test)",
        "    print(f\"'{test}' -> {result}\")"
    ], "Parentheses validation with stack")
    
    check_interactive_mode()
    
    # Challenge 6: Reverse a Linked List (Simulated with List)
    print("\n🔄 Challenge 6: Reverse a List")
    print("-" * 30)
    print("Reverse a list in-place and create a new reversed list")
    
    def reverse_list_inplace(lst):
        """Reverse a list in-place."""
        left, right = 0, len(lst) - 1
        while left < right:
            lst[left], lst[right] = lst[right], lst[left]
            left += 1
            right -= 1
        return lst
    
    def reverse_list_new(lst):
        """Create a new reversed list."""
        return lst[::-1]
    
    original = [1, 2, 3, 4, 5]
    
    # In-place reversal
    in_place_copy = original.copy()
    reverse_list_inplace(in_place_copy)
    print(f"Original: {original}")
    print(f"Reversed in-place: {in_place_copy}")
    
    # New reversed list
    new_reversed = reverse_list_new(original)
    print(f"New reversed list: {new_reversed}")
    
    snippet_section([
        "# Reverse List In-Place",
        "def reverse_list_inplace(lst):",
        "    left, right = 0, len(lst) - 1",
        "    while left < right:",
        "        lst[left], lst[right] = lst[right], lst[left]",
        "        left += 1",
        "        right -= 1",
        "    return lst",
        "",
        f"original = {original}",
        "copy_list = original.copy()",
        "reversed_list = reverse_list_inplace(copy_list)",
        "print(f'Reversed: {reversed_list}')"
    ], "In-place list reversal")
    
    check_interactive_mode()
    
    # Challenge 7: Binary Search
    print("\n🔍 Challenge 7: Binary Search")
    print("-" * 30)
    print("Find element in sorted array using binary search")
    
    def binary_search(arr, target):
        """Binary search implementation."""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1
    
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    targets = [7, 4, 19, 1]
    
    print(f"Sorted array: {sorted_array}")
    for target in targets:
        index = binary_search(sorted_array, target)
        if index != -1:
            print(f"Target {target} found at index {index}")
        else:
            print(f"Target {target} not found")
    
    snippet_section([
        "# Binary Search",
        "def binary_search(arr, target):",
        "    left, right = 0, len(arr) - 1",
        "    while left <= right:",
        "        mid = (left + right) // 2",
        "        if arr[mid] == target:",
        "            return mid",
        "        elif arr[mid] < target:",
        "            left = mid + 1",
        "        else:",
        "            right = mid - 1",
        "    return -1",
        "",
        f"arr = {sorted_array}",
        "target = 7",
        "index = binary_search(arr, target)",
        "print(f'Found at index: {index}')"
    ], "Binary search algorithm")
    
    check_interactive_mode()
    
    # Challenge 8: Anagram Detection
    print("\n🔤 Challenge 8: Anagram Detection")
    print("-" * 30)
    print("Check if two strings are anagrams of each other")
    
    def are_anagrams(str1, str2):
        """Check if two strings are anagrams."""
        # Remove spaces and convert to lowercase
        str1_clean = str1.replace(' ', '').lower()
        str2_clean = str2.replace(' ', '').lower()
        
        # Check if lengths are different
        if len(str1_clean) != len(str2_clean):
            return False
        
        # Count frequency of each character
        char_count = {}
        
        # Count characters in first string
        for char in str1_clean:
            char_count[char] = char_count.get(char, 0) + 1
        
        # Subtract counts for second string
        for char in str2_clean:
            if char not in char_count:
                return False
            char_count[char] -= 1
            if char_count[char] == 0:
                del char_count[char]
        
        return len(char_count) == 0
    
    test_pairs = [
        ("listen", "silent"),
        ("elbow", "below"),
        ("hello", "world"),
        ("The Eyes", "They See")
    ]
    
    for str1, str2 in test_pairs:
        result = are_anagrams(str1, str2)
        print(f"'{str1}' & '{str2}' -> {result}")
    
    snippet_section([
        "# Anagram Detection",
        "def are_anagrams(str1, str2):",
        "    str1_clean = str1.replace(' ', '').lower()",
        "    str2_clean = str2.replace(' ', '').lower()",
        "    if len(str1_clean) != len(str2_clean):",
        "        return False",
        "    char_count = {}",
        "    for char in str1_clean:",
        "        char_count[char] = char_count.get(char, 0) + 1",
        "    for char in str2_clean:",
        "        if char not in char_count:",
        "            return False",
        "        char_count[char] -= 1",
        "        if char_count[char] == 0:",
        "            del char_count[char]",
        "    return len(char_count) == 0",
        "",
        "print(are_anagrams('listen', 'silent'))"
    ], "Anagram detection with character counting")
    
    check_interactive_mode()
    
    # Challenge 9: Remove Duplicates from Sorted Array
    print("\n🗑️ Challenge 9: Remove Duplicates")
    print("-" * 30)
    print("Remove duplicates from sorted array in-place")
    
    def remove_duplicates(nums):
        """Remove duplicates from sorted array in-place."""
        if not nums:
            return 0
        
        write_index = 1
        
        for read_index in range(1, len(nums)):
            if nums[read_index] != nums[read_index - 1]:
                nums[write_index] = nums[read_index]
                write_index += 1
        
        return write_index
    
    test_array = [1, 1, 2, 2, 2, 3, 4, 4, 5]
    original_array = test_array.copy()
    
    new_length = remove_duplicates(test_array)
    unique_elements = test_array[:new_length]
    
    print(f"Original array: {original_array}")
    print(f"After removing duplicates: {unique_elements}")
    print(f"New length: {new_length}")
    
    snippet_section([
        "# Remove Duplicates from Sorted Array",
        "def remove_duplicates(nums):",
        "    if not nums:",
        "        return 0",
        "    write_index = 1",
        "    for read_index in range(1, len(nums)):",
        "        if nums[read_index] != nums[read_index - 1]:",
        "            nums[write_index] = nums[read_index]",
        "            write_index += 1",
        "    return write_index",
        "",
        f"nums = {original_array}",
        "new_length = remove_duplicates(nums)",
        "unique = nums[:new_length]",
        "print(f'Unique elements: {unique}')"
    ], "In-place duplicate removal")
    
    check_interactive_mode()
    
    # Challenge 10: Climbing Stairs (Dynamic Programming)
    print("\n🪜 Challenge 10: Climbing Stairs")
    print("-" * 30)
    print("Count ways to climb stairs (1 or 2 steps at a time)")
    
    def climb_stairs_memoized(n, memo=None):
        """Count ways to climb n stairs with memoization."""
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 2:
            return n
        
        memo[n] = climb_stairs_memoized(n-1, memo) + climb_stairs_memoized(n-2, memo)
        return memo[n]
    
    def climb_stairs_iterative(n):
        """Count ways to climb n stairs iteratively."""
        if n <= 2:
            return n
        
        prev2, prev1 = 1, 2
        
        for i in range(3, n + 1):
            current = prev1 + prev2
            prev2, prev1 = prev1, current
        
        return prev1
    
    for steps in [3, 5, 8]:
        memoized_result = climb_stairs_memoized(steps)
        iterative_result = climb_stairs_iterative(steps)
        print(f"Ways to climb {steps} stairs: {memoized_result} (both methods agree: {memoized_result == iterative_result})")
    
    snippet_section([
        "# Climbing Stairs with Memoization",
        "def climb_stairs_memoized(n, memo=None):",
        "    if memo is None:",
        "        memo = {}",
        "    if n in memo:",
        "        return memo[n]",
        "    if n <= 2:",
        "        return n",
        "    memo[n] = climb_stairs_memoized(n-1, memo) + climb_stairs_memoized(n-2, memo)",
        "    return memo[n]",
        "",
        "steps = 5",
        "ways = climb_stairs_memoized(steps)",
        "print(f'Ways to climb {steps} stairs: {ways}')"
    ], "Dynamic programming with memoization")
    
    check_interactive_mode()
    
    print("\n🎉 Challenges Complete!")
    print("=" * 50)
    print("You've practiced 10 fundamental programming challenges:")
    print("1. Fibonacci (Memoization)")
    print("2. Two Sum (Hash Maps)")
    print("3. Palindrome Check (String Processing)")
    print("4. Maximum Subarray (Kadane's Algorithm)")
    print("5. Valid Parentheses (Stack)")
    print("6. Reverse List (Two Pointers)")
    print("7. Binary Search (Divide & Conquer)")
    print("8. Anagram Detection (Character Counting)")
    print("9. Remove Duplicates (Two Pointers)")
    print("10. Climbing Stairs (Dynamic Programming)")
    print()
    print("💡 Key Techniques Learned:")
    print("   • Memoization for optimization")
    print("   • Hash maps for fast lookups")
    print("   • Two pointers technique")
    print("   • Stack for matching problems")
    print("   • Dynamic programming")
    print("   • Divide and conquer")
    print()
    print("🚀 Ready for more advanced challenges!")

    if step:
        step_through_function(challenges_block, globals(), locals())
    else:
        challenges_block()

# Module metadata
DESCRIPTION = 'Programming Challenges and Problem Solving'
FUNCTION = challenges_module