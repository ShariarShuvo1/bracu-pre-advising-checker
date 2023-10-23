function FilterBar() {
    return (
        <div className="bg-blue-950 text-amber-50">
            <ul className="items-center w-full text-sm font-medium text-gray-900 bg-blue-100 border sm:flex">
                <li className="w-full sm:border-b-0 sm:border-r hover:bg-blue-200 hover:rounded-lg">
                    <div className="flex items-center pl-3">
                        <input id="disable-seat-limit" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"/>
                        <label htmlFor="disable-seat-limit" className="w-full py-3 ml-2 text-sm font-medium text-gray-900">Disable Seat Limit</label>
                    </div>
                </li>
                <li className="w-full sm:border-b-0 sm:border-r hover:bg-blue-200 hover:rounded-lg">
                    <div className="flex items-center pl-3">
                        <input id="allow-same-course" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"/>
                        <label htmlFor="allow-same-course" className="w-full py-3 ml-2 text-sm font-medium text-gray-900">Allow Same Course</label>
                    </div>
                </li>
                <li className="w-full sm:border-b-0 sm:border-r hover:bg-blue-200 hover:rounded-lg">
                    <div className="flex items-center pl-3">
                        <input id="allow-exam-clash" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"/>
                        <label htmlFor="allow-exam-clash" className="w-full py-3 ml-2 text-sm font-medium text-gray-900">Allow Exam Clash</label>
                    </div>
                </li>
                <li className="w-full sm:border-b-0 sm:border-r hover:bg-blue-200 hover:rounded-lg">
                    <div className="flex items-center pl-3">
                        <input id="allow-theory-clash" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"/>
                        <label htmlFor="allow-theory-clash" className="w-full py-3 ml-2 text-sm font-medium text-gray-900">Allow Theory Clash</label>
                    </div>
                </li>
                <li className="w-full sm:border-b-0 sm:border-r hover:bg-blue-200 hover:rounded-lg">
                    <div className="flex items-center pl-3">
                        <input defaultChecked id="allow-lab-clash" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"/>
                        <label htmlFor="allow-lab-clash" className="w-full py-3 ml-2 text-sm font-medium text-gray-900">Allow Lab Clash</label>
                    </div>
                </li>
                <li className="w-full sm:border-b-0 sm:border-r hover:bg-blue-200 hover:rounded-lg">
                    <div className="flex items-center pl-3">
                        <input id="disable-all-restriction" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"/>
                        <label htmlFor="disable-all-restriction" className="w-full py-3 ml-2 text-sm font-medium text-gray-900">Disable All Restriction</label>
                    </div>
                </li>
            </ul>
        </div>
    );
}

export default FilterBar;
