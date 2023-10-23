function Navbar() {
    return (
        <>
            <div className="flex flex-wrap bg-black text-white text-2xl items-center justify-between mx-auto">
                <p className="ml-1 bg-gradient-to-r from-purple-600 to-blue-500 inline-block text-transparent bg-clip-text">
                    BRACU Pre-Advising Checker
                </p>
                <button className="relative inline-flex items-center justify-center p-0.5 mb-1 mr-2 mt-1 overflow-hidden text-sm font-medium rounded-lg group bg-gradient-to-br from-purple-600 to-blue-500 group-hover:from-purple-600 group-hover:to-blue-500 hover:text-white text-white focus:ring-4 focus:outline-none focus:ring-blue-800">
                  <span className="relative px-5 py-2.5 transition-all ease-in duration-75 bg-gray-900 rounded-md group-hover:bg-opacity-0">
                      Advance Mode
                  </span>
                </button>
            </div>
        </>
    );
}

export default Navbar;
