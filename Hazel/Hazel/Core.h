#pragma once

#include "Application.h"

#ifdef Windows_run
	
	#ifdef HZ_dll
		#define HZ_app : __decspec(dllexport) 
	#else
		#define HZ_app : __decspec(dllimport)

#else error "wrong os"

#endif