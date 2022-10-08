#pragma once
// Class header file used for containning the implementaion of the class
// the name of file should be the same with cpp file

// classname::method
// class name denotes which class this method belongs to
// method equals to the class method

namespace Hazel {

	class Application
	{
	public:
		// constructor
		Application();
		// destructor
		virtual ~Application();
		// run application
		void Run();
	};

};