## CXX_Class  

## Content  

* [class](#Class)  
* [polymorphism](#Polymorphism)  
* [datastruct](#Data_Structure)  

## Class  

* Syntax  
1. class initialization
2. friend class / function
3. public / protected / private
4. const function / const return type

```cpp

// forward declaration
class C;
void dongle(A& a);

class A
{
  // Allow class C to access class A private var & func 
  friend class C;

  // Allow function dongle to access class A private data
  friend void dongle(A& a);
 
  // All user can call this member variable & member func
  public:
  A(int ia) : a(ia) {};

  // We can initialize member var;
  int a = 1;
  int foo();

  // const syntax means this function wont modify object A
  int frozen(const C& c) const;
  
  // const return type and specifier is needed for const object A
  // ex. const A *a;
  //     const int *aa = a->getA();
  //     a->foo() <--- compile error
  const int* getA() const { return *a; };

  // All class A object share this static variable, Class variable
  static int b;

  // Class function (no object info), method, A::bangle(c)
  static int bangle(const C& c);

  // Only children and parent class can call this member variable & func
  protected:
  int b;
  int bar();

  // Only class itself can use it (internally)
  private:
  int c;
  int cat();
  
}

// Class static variable must define outside the class;
int A::b = 1;
```

## Polymorphism  

* Syntax
1. virtual func = delete, func = 0
2. upcasting/ downcasting

```cpp
class A
{
  public:
  A() { cout << "I am A a is " << a << endl; };
  void foo() { a = 2 };
  
  // pure virtual function, children class must override function to allow instantiation
  virtual void bar() = 0;
  int a = 1;
}

class B
{
  public:
  B() { cout << "I am B a is " << a << endl; };
  void foo() { a = 2 };
  
  // Default delete function, if there is no override, when doing down casting,
  // Parent class cannot call this function (get deleted)
  virtual void bar() = delete;
  int a = 1;
}

class Ctest : public A
{
  public:
  Ctest() { cout << "I am Ctest " << endl; };
}

class Btest : pulic B
{
  public:
  Btest() { cout << "I am Btest " << endl; };
}

class C : public A
{
  public:
  C() { cout << "I am C\n"; };
  void bar() override { "I am C a is " << a << endl; };
}

int main()
{
  Ctest ct; // Compile error for pure virtual function bar() not defined.
  A a; // Compile error for virtual class
  B b; // Compile error as well
  C c; // OK Inherit A constructor, print "I am A a is 1\nI am C\n"
  c.bar(); // print "I am C a is 1\n"
  Btest bt; // Ok as B::bar() = delete
  // B *b = &bt; // OK downcast
  B *b = dynamic_cast<B*>(&bt) // OK downcast
  if (b == nullptr) // OK Check if downcast fail
    return -1;
  b->bar() // Compile error as bar() is deleted as there is no override
}
```  

## Data_Structure  

* [reference](https://www.bigocheatsheet.com/)  

* vector
1. O1 push_back
2. O1 pop_back
3. O1 element access
4. ON search
5. When there is random erase() / insertion, it destroy O1 erase, iterator -> become list

* list
1. linked list
2. O1 push_back / pop_back
3. ON search
4. ON/2 element access/ erase/ random insertion

* stack
1. like vector, but first in last out

* queue
1. like vector, but always first in first out

* priority queue
1. like queue, but using balance binary tree to do sorting and accessment

* array
1. static element allocation
2. Cannot destroy, erase, insert
3. O1 access
4. ON search

* set
1. O1 search
2. ON access
3. ON insertion, deletion
4. unique keys only

* map (binary search tree)
1. O(logn) search
2. O(logn) insertion
3. O(logn) deletion
4. sorted
5. similar to set, have key, value pair
6. cannot have same key

* unordered_map (hash table, dict)
1. O(1) search
2. O(1) insertion
3. O(1) deletion
4. unsorted
