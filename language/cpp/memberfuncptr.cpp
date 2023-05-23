/* This cpp is to demonstrate how to call non-static member function ptr from other class 
 * class ThreadFunc calls member function pointer mAction by class object mFoo
 *                   (mFoo->*mAction)(args)
 */

#include <iostream>
#include <string>

using namespace std;

class Options {
    public:
        bool mA = true;
        bool mB = false;
};

class Foo {
    public:

    bool test(const Options& options){ cout << "ma*3 is " << ma * 3  << "\n"; return true; };

    int ma=3;
    int mb;
};

class ThreadFunc {

    typedef bool (Foo::* Action)(const Options& options);

public:

    ThreadFunc (Foo* foo, Action action, const Options& options)
        : mFoo(foo), mAction(action), mOptions(options)
    {}
    void run(void)
    {
        (mFoo->*mAction)(mOptions);
    }

    static void* run(void *arg)
    {
        ThreadFunc *func = static_cast<ThreadFunc*>(arg);
        func->run();
        return 0;
    }

    Foo* mFoo;
    Action mAction;
    const Options& mOptions;
};


int main()
{
    Foo *foo = new Foo;
    Foo *foo1 = new Foo;
    foo->ma = 5;
    Options opt;

    ThreadFunc *func = new ThreadFunc(foo, &Foo::test, opt);
    ThreadFunc *func1 = new ThreadFunc(foo1, &Foo::test, opt);
    ThreadFunc::run(func); // print "ma*3 is 15"
    ThreadFunc::run(func1); // print "ma*3 is 9"
    delete func;
    delete func1;
    delete foo;
    delete foo1;
    return 0;
}
