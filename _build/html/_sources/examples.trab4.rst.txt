examples.trab4 module
=====================

.. automodule:: examples.trab4
   :members:
   :undoc-members:
   :show-inheritance:

.. code-block:: python

    assume m >= 0 and n >= 0 and r == 0 and x == m and y == n
    0: while y > 0:
    1:    if y & 1 == 1:
                y , r  = y-1 , r+x
    2:    x , y = x<<1  ,  y>>1
    3: assert r == m * n

In our notation each proposition :math:`P` has variables. Each variable is indexed (by
convention we index at :math:`0` or :math:`1` for next variables in transition
relation). For example, if :math:`T ≡ x' = x + 1` we would write :math:`T ≡ x[1] = x[0]
+ 1`.

We write :math:`T[k]` to mean :math:`T` with :math:`k` added to the index of each
variable.

In the example above :math:`T[k] ≡ x[k+1] = x[k] + 1`.

So the state space after one transition from initial state is :math:`I[0] ∧ T[0]`.

Furthermore, :math:`T[:k] ≡ \bigwedge_{i=0}^{k} T[k]`

Properties

.. math:: V ≡ (y - pc) + 3
.. math:: \textrm{nonnegative} ≡ V ≥ 0
.. math:: \textrm{decreasing} ≡ \bigwedge_{i=0}^{2}T(i,i+1) ⟹ V(3) ≤ V(0) ∨ V(3) = 0
.. math:: \textrm{termination} ≡ V = 0 ⟹ pc=3
.. math:: \textrm{INV} ≡ (m ⋅ n = x ⋅ y + r) ∧ y ≥ 0

First we need to define some variables

.. code-block::

    bit_count = 4
    x = Predicate(Variable('x', BVType(bit_count)))
    m = Predicate(Variable("m", BVType(bit_count)))
    n = Predicate(Variable("n", BVType(bit_count)))
    y = Predicate(Variable("y", BVType(bit_count)))
    r = Predicate(Variable("r", BVType(bit_count)))
    pc = Predicate(Variable('pc', BVType(bit_count)))

Then we define a helper function `t()` to add :math:`v'=v` to the transitions.

.. code-block::

    variables = {x, y, r, m, n, pc}
    # Variables not in s are unchanged
    t = lambda s: And([v[1].Equals(v[0]) for v in variables if v not in s])

Now we can start defining the transition relation:

The WHILE condition can be defined as:

.. code-block::

    WhileCondition = Predicate(y[0] > 0)

- WHILE condition is True (:math:`pc = 0 ∧ pc' = 1 ∧ \textrm{WhileCondition}`):
    .. code-block::

        p1 = And(
            pc[0].Equals(0),
            pc[1].Equals(1),
            WhileCondition[0],
            t({pc})
        )

- WHILE condition is False (:math:`pc = 0 ∧ pc' = 3 ∧ ¬\textrm{WhileCondition}`):
    .. code-block::

        p2 = And(
            pc[0].Equals(0),
            pc[1].Equals(3),
            ~WhileCondition[0],
            t({pc})
        )

The IF condition can be written as:
    .. code-block::

        IfCondition = Predicate((y[0] & 1).Equals(1))

Then

- IF condition is True (:math:`pc = 1 ∧ pc' = 2 ∧ \textrm{IfCondition} ∧ y' = y − 1 ∧ r' = r + x`):
    .. code-block::

        p3 = And(
            pc[0].Equals(1),
            pc[1].Equals(2),
            IfCondition[0],
            y[1].Equals(y[0] - 1),
            r[1].Equals(r[0] + x[0]),
            t({pc, y, r})
        )

- IF condition is False (:math:`pc = 1 ∧ pc' = 2 ∧ ¬\textrm{IfCondition}`):
    .. code-block::

        p4 = And(
            pc[0].Equals(1),
            pc[1].Equals(2),
            ~IfCondition[0],
            t({pc})
        )

- execute rest of WHILE body and loop back to condition check (:math:`pc = 2 ∧ pc' = 0 ∧ y' = y ≫ 1 ∧ x' = x ≪ 1`)
    .. code-block::

        p5 = And(
            pc[0].Equals(2),
            pc[1].Equals(0),
            x[1].Equals(x[0] << 1),
            y[1].Equals(y[0] >> 1),
            t({pc, x, y})
        )

- end of program (:math:`pc = 3 ∧ pc' = 3`):
    .. code-block::

        p6 = pc[0].Equals(3) & t({})

Finally create the transition relation:

.. code-block::

    trans = Or(p1, p2, p3, p4, p5, p6)
    T = Predicate(trans)

Establish the precondition:

.. code-block::

   pre = And(
        (m[0] >= 0),  # m ≥ 0
        (n[0] >= 0),  # n ≥ 0
        r[0].Equals(0),  # r = 0
        x[0].Equals(m[0]),  # x = m
        y[0].Equals(n[0])  # y = n
    )

Our postcondition:

.. code-block::

    post = r[0].Equals(m[0] * n[0])

The initial state:

.. code-block::

    init = pc[0].Equals(0) & pre
    I = Predicate(init)

We are going to stipulate a variant

.. code-block::

    V = Predicate((y[0] - pc[0]) + 3)

Because we are working in the theory of bit vectors we can have overflows.
We are working in the theory of bit vectors because no interpolator is available in
pySMT when bit vectors are mixed with integers.

.. code-block::

    overflow_condition_for_variant = 2 ** bit_count - 3

Finally we can encode the properties we desire to prove

.. code-block::

    overflow_condition_for_variant = 2 ** bit_count - 3
    variant_is_non_negative = V[0] >= 0
    variant_is_strictly_decreasing = (
            T[0:2] &
            (y[0] < overflow_condition_for_variant)).Implies(
        (V[3] < V[0]) | V[3].Equals(0))
    variant_equals_zero_implies_termination = (
        (V[0].Equals(0) &
         (y[0] < overflow_condition_for_variant)).Implies(
            pc[0].Equals(3)))

    invariant = (m[0] * n[0]).Equals(x[0] * y[0] + r[0]) & (y[0] >= 0)
    precondition_implies_invariant = pre.Implies(invariant)
    loop_termination_implies_postcondition = (
            invariant &
            (~WhileCondition[0])).Implies(post)
    invariant_is_true_after_loop = ...
    wrong_prop = (n[0].NotEquals(0) & pc[0].Equals(3)).Implies(y[0].NotEquals(0))
    wrong_prop2 = (n[0].Equals(12) & pc[0].Equals(3)).Implies(y[0].NotEquals(0))

Then we can execute

.. code-block::

        properties = [
        (variant_is_non_negative, "variant_is_non_negative"),
        (variant_is_strictly_decreasing, "variant_is_strictly_decreasing"),
        (variant_equals_zero_implies_termination, "variant_equals_zero_implies_termination"),
        (precondition_implies_invariant, "precondition_implies_invariant"),
        (loop_termination_implies_postcondition, "loop_termination_implies_postcondition"),
        (wrong_prop, "wrong_prop"),
        (wrong_prop2, "wrong_prop2"),
    ]

    for algo in [PDR, IMC]:
        print(f"Using {algo.__name__}:")
        for prop, prop_name in properties:
            print(f"proving {prop_name}")
            print(PDR(I, T, Predicate(prop)))

The code can be executed obtaining:

.. execute_code::
    :hide_code:
    :hide_headers:

   from examples.trab4 import main
   main()

