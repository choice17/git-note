## void func() const
 
 - it only matters for member function, **only const object can call const function**

```
class A
{
public:
  void Const_No();   // nonconst member function
  void Const_Yes() const; // const member function
};


A  obj_nonconst;  // nonconst object
obj_nonconst.Const_No();  // works fine
obj_nonconst.Const_Yes(); // works fine

const A obj_const = A(); // const object
obj_const.Const_Yes(); // works fine (const object can call const function)
obj_const.Const_No();  // ERROR (const object cannot call nonconst function)

```

 - while void const f() is equivilent to const void f(), it makes no sense as void itself return nothing