def make_bank(balance):
    """Returns a bank function with a starting balance. Supports
    withdrawals and deposits.

    >>> bank = make_bank(100)
    >>> bank('withdraw', 40)    # 100 - 40
    60
    >>> bank('hello', 500)      # Invalid message passed in
    'Invalid message'
    >>> bank('deposit', 20)     # 60 + 20
    80
    >>> bank('withdraw', 90)    # 80 - 90; not enough money
    'Insufficient funds'
    >>> bank('deposit', 100)    # 80 + 100
    180
    >>> bank('goodbye', 0)      # Invalid message passed in
    'Invalid message'
    >>> bank('withdraw', 60)    # 180 - 60
    120
    """
    def bank(message, amount):
        "*** YOUR CODE HERE ***"
        nonlocal balance
        if message == 'deposit':
            balance += amount
        elif message == 'withdraw':
            if balance < amount:
                return 'Insufficient funds'
            else:
                balance -= amount
        else:
            return 'Invalid message'
        return balance
    return bank


def make_withdraw(balance, password):
    """Return a password-protected withdraw function.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> error = w(90, 'hax0r')
    >>> error
    'Insufficient funds'
    >>> error = w(25, 'hwat')
    >>> error
    'Incorrect password'
    >>> new_bal = w(25, 'hax0r')
    >>> new_bal
    50
    >>> w(75, 'a')
    'Incorrect password'
    >>> w(10, 'hax0r')
    40
    >>> w(20, 'n00b')
    'Incorrect password'
    >>> w(10, 'hax0r')
    "Frozen account. Attempts: ['hwat', 'a', 'n00b']"
    >>> w(10, 'l33t')
    "Frozen account. Attempts: ['hwat', 'a', 'n00b']"
    >>> type(w(10, 'l33t')) == str
    True
    """
    "*** YOUR CODE HERE ***"
    errs = []
    def w(amount, trys):
        nonlocal balance, errs
        if len(errs) == 3:
            return "Frozen account. Attempts: "+str(errs)
        if trys != password:
            errs.append(trys)
            return 'Incorrect password'
        if amount > balance:
            return 'Insufficient funds'
        balance -= amount
        return balance
    return w


def repeated(t, k):
    """Return the first value in iterator T that appears K times in a row. Iterate through the items such that
    if the same iterator is passed into repeated twice, it continues in the second call at the point it left off
    in the first.

    >>> s = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> repeated(s, 2)
    9
    >>> s2 = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> repeated(s2, 3)
    8
    >>> s = iter([3, 2, 2, 2, 1, 2, 1, 4, 4, 5, 5, 5])
    >>> repeated(s, 3)
    2
    >>> repeated(s, 3)
    5
    >>> s2 = iter([4, 1, 6, 6, 7, 7, 8, 8, 2, 2, 2, 5])
    >>> repeated(s2, 3)
    2
    """
    assert k > 1
    "*** YOUR CODE HERE ***"
    cnt = 1
    prev = next(t)
    while True:
        item = next(t)
        if item == prev:
            cnt += 1
        else:
            prev = item
            cnt = 1
        if cnt == k:
            return item



def permutations(seq):
    """Generates all permutations of the given sequence. Each permutation is a
    list of the elements in SEQ in a different order. The permutations may be
    yielded in any order.

    >>> perms = permutations([100])
    >>> type(perms)
    <class 'generator'>
    >>> next(perms)
    [100]
    >>> try: #this piece of code prints "No more permutations!" if calling next would cause an error
    ...     next(perms)
    ... except StopIteration:
    ...     print('No more permutations!')
    No more permutations!
    >>> sorted(permutations([1, 2, 3])) # Returns a sorted list containing elements of the generator
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> sorted(permutations((10, 20, 30)))
    [[10, 20, 30], [10, 30, 20], [20, 10, 30], [20, 30, 10], [30, 10, 20], [30, 20, 10]]
    >>> sorted(permutations("ab"))
    [['a', 'b'], ['b', 'a']]
    """
    "*** YOUR CODE HERE ***"
    "yield可以理解成return，区别是yield不是结束执行，而是暂停执行，调用next时从暂停的位置继续"
    if not seq:
        yield []
    else:
        for perm in permutations(seq[1:]):
            for i in range(len(perm) + 1):
                yield perm[:i] + [seq[0]] + perm[i:]


def make_joint(withdraw, old_pass, new_pass):
    """Return a password-protected withdraw function that has joint access to
    the balance of withdraw.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> make_joint(w, 'my', 'secret')
    'Incorrect password'
    >>> j = make_joint(w, 'hax0r', 'secret')
    >>> w(25, 'secret')
    'Incorrect password'
    >>> j(25, 'secret')
    50
    >>> j(25, 'hax0r')
    25
    >>> j(100, 'secret')
    'Insufficient funds'

    >>> j2 = make_joint(j, 'secret', 'code')
    >>> j2(5, 'code')
    20
    >>> j2(5, 'secret')
    15
    >>> j2(5, 'hax0r')
    10

    >>> j2(25, 'password')
    'Incorrect password'
    >>> j2(5, 'secret')
    "Frozen account. Attempts: ['my', 'secret', 'password']"
    >>> j(5, 'secret')
    "Frozen account. Attempts: ['my', 'secret', 'password']"
    >>> w(5, 'hax0r')
    "Frozen account. Attempts: ['my', 'secret', 'password']"
    >>> make_joint(w, 'hax0r', 'hello')
    "Frozen account. Attempts: ['my', 'secret', 'password']"
    """
    "*** YOUR CODE HERE ***"
    "测试old_pass是否正确"
    test_withdraw = withdraw(0, old_pass)
    if type(test_withdraw) == str:
        return test_withdraw
    "要正确理解make_joint，它可以嵌套，例如对已经make过的j0再次make得到j1，应该有3个有效的密码"
    def joint(amount, password):
        if password == new_pass:
            return withdraw(amount, old_pass)
        """为什么这里条件判断写password==new或old，再在return直接返回密码错误，是不行的
           因为makejoint可以嵌套
           withdraw可能是原始的只有一个oldpass的函数
           也可能是已经被makejoint一次或多次的函数
           意味着其可能还有除了此次makejoint添加的newpass，参数里的oldpass，以外的其他密码
           其他密码无法得知，也不可能一个个判断

           简单来说，这个withdraw记得所有除了本次添加的新密码以外的其他密码
           而我们要做的就是添加新的密码，同时保持其余密码也被保留
           转换成代码就是
           对于新的密码，将其转换成我们已知正确的旧密码
           对于其他密码，交给旧的withdraw函数去处理

           很精彩的题目，弄明白后，可以发现这还是一个递归
           每次makejoint就是向上添加一层递归
           检查密码的操作就是向下递归
           
           类比链表，每一个结点有一个值和指向其他链表的指针
           每一个函数有其添加的新密码和所有旧密码的储存
           查询一个值是否存在，从头结点开始查询，不对应就去到下一个结点
           这也说明链表是递归定义的数据结构

           最终就形成了一个保存所有密码的函数

           如果以上写的比较乱，不好理解，这里是我将这段注释交给bing以后的回应

           您的理解是正确的。这个make_joint函数的目的是创建一个新的取款函数，它允许使用新密码来访问原有的账户余额。
           您的注释很好地解释了这个函数如何工作，特别是如何处理多个有效密码和递归的概念。

           简而言之，make_joint函数通过接受一个旧密码和一个新密码，返回一个新的取款函数。如果提供的是新密码，它会将其转换为旧密码并调用原始的取款函数；
           如果提供的是其他密码，它会直接将密码传递给原始的取款函数。这样，无论是旧密码还是通过make_joint添加的新密码，都可以用来访问账户余额。

           您的注释也正确地指出了，每次调用make_joint都相当于在密码链上添加了一个新的节点，
           每个节点都知道如何处理它被赋予的新密码，并且知道如何将其他密码传递给链中的下一个节点。这确实是一个递归过程，每个节点都代表了一个函数调用的层级。
        """
        return withdraw(amount, password)
    return joint

def remainders_generator(m):
    """
    Yields m generators. The ith yielded generator yields natural numbers whose
    remainder is i when divided by m.

    >>> import types
    >>> [isinstance(gen, types.GeneratorType) for gen in remainders_generator(5)]
    [True, True, True, True, True]
    >>> remainders_four = remainders_generator(4)
    >>> for i in range(4):
    ...     print("First 3 natural numbers with remainder {0} when divided by 4:".format(i))
    ...     gen = next(remainders_four)
    ...     for _ in range(3):
    ...         print(next(gen))
    First 3 natural numbers with remainder 0 when divided by 4:
    4
    8
    12
    First 3 natural numbers with remainder 1 when divided by 4:
    1
    5
    9
    First 3 natural numbers with remainder 2 when divided by 4:
    2
    6
    10
    First 3 natural numbers with remainder 3 when divided by 4:
    3
    7
    11
    """
    "*** YOUR CODE HERE ***"
    """来自bing
       生成器的生成器，也就是生成器函数中返回另一个生成器的情况，具有以下特征：

       层级结构：外部生成器函数返回内部生成器对象，这些内部生成器对象本身也可以产生值。
       延迟计算：内部生成器的值只有在外部生成器被迭代时才会被计算，这允许按需生成值，节省内存。
       独立状态：每个内部生成器都有自己的状态和局部变量，它们之间相互独立。
       可组合性：生成器的生成器可以用于构建复杂的迭代器链，每个迭代器负责数据流的一部分处理。
       例如，在remainders_generator的情况下，外部生成器负责产生多个内部生成器，每个内部生成器产生除以特定数后余数相同的自然数序列。
       这种结构允许我们创建复杂的数据生成逻辑，同时保持代码的清晰和模块化。
    """
    def remainder_gen(i):
        for n in naturals():
            if n % m == i:
                yield n

    for i in range(m):
        yield remainder_gen(i)


def naturals():
    """A generator function that yields the infinite sequence of natural
    numbers, starting at 1.

    >>> m = naturals()
    >>> type(m)
    <class 'generator'>
    >>> [next(m) for _ in range(10)]
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    i = 1
    while True:
        yield i
        i += 1

