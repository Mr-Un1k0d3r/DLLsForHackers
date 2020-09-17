# DLLsForHackers
Dlls that can be used for side loading and other attack vectors.

# Why?

I've seen to many POC with code been executed in the `DLL_PROCESS_ATTACH`. In fact most of the of the time the malcious code will not work as stated by Microsoft (https://docs.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-best-practices).

You should never perform the following tasks from within DllMain:

*    Call LoadLibrary or LoadLibraryEx (either directly or indirectly). This can cause a deadlock or a crash.
*    Call GetStringTypeA, GetStringTypeEx, or GetStringTypeW (either directly or indirectly). This can cause a deadlock or a crash.
*    Synchronize with other threads. This can cause a deadlock.
*    Acquire a synchronization object that is owned by code that is waiting to acquire the loader lock. This can cause a deadlock.
*    Initialize COM threads by using CoInitializeEx. Under certain conditions, this function can call LoadLibraryEx.
*    Call the registry functions. These functions are implemented in Advapi32.dll. If Advapi32.dll is not initialized before your DLL, the DLL can access uninitialized memory and cause the process to crash.
*    Call CreateProcess. Creating a process can load another DLL.
*    Call ExitThread. Exiting a thread during DLL detach can cause the loader lock to be acquired again, causing a deadlock or a crash.
*    Call CreateThread. Creating a thread can work if you do not synchronize with other threads, but it is risky.
*    Create a named pipe or other named object (Windows 2000 only). In Windows 2000, named objects are provided by the Terminal Services DLL. If this DLL is not initialized, calls to the DLL can cause the process to crash.
*    Use the memory management function from the dynamic C Run-Time (CRT). If the CRT DLL is not initialized, calls to these functions can cause the process to crash.
*    Call functions in User32.dll or Gdi32.dll. Some functions load another DLL, which may not be initialized.
    Use managed code.
    
 ## Only the following are considered safe
 
 The following tasks are safe to perform within DllMain:

*    Initialize static data structures and members at compile time.
*    Create and initialize synchronization objects.
*    Allocate memory and initialize dynamic data structures (avoiding the functions listed above.)
*    Set up thread local storage (TLS).
*    Open, read from, and write to files.
*    Call functions in Kernel32.dll (except the functions that are listed above).
*    Set global pointers to NULL, putting off the initialization of dynamic members. In Microsoft Windows Vista™, you can use the one-time initialization functions to ensure that a block of code is executed only once in a multithreaded environment.

# Usage

# Compile it using GCC

* Exec (exec.c)
```
mingw32-g++.exe -Wall -DBUILD_DLL -O2  -c exec.c -o exec.o
mingw32-g++.exe -shared -Wl,--dll  exec.o  -o exec.dll
```

* Drop Exec (dropexec.c)
```
mingw32-g++.exe -Wall -DBUILD_DLL -O2  -c dropexec.c -o dropexec.o
mingw32-g++.exe -shared -Wl,--dll  dropexec.o  -o dropexec.dll
```

# Credit

Mr.Un1k0d3r RingZer0 Team
