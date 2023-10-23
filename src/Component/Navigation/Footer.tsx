function Footer() {
    return (
        <>
            <div className="bg-blue-100 fixed inset-x-0 bottom-0">
                <div className="flex flex-wrap items-center justify-between mx-auto mt-1 ml-2 mr-2">
                    <p>
                        Created By:
                        <a className="text-fuchsia-500 hover:text-fuchsia-900 hover:bg-blue-300 hover:rounded" href="https://www.facebook.com/ShariarShuvo01/" target="_blank"> Shariar Islam Shuvo</a>
                    </p>
                    <a className="flex text-fuchsia-500 hover:text-fuchsia-900 hover:bg-blue-300 hover:rounded" href="https://github.com/ShariarShuvo1/bracu-pre-advising-checker" target="_blank">
                        <img className="object-cover h-5 w-5 mr-1 mt-0.5" src={require("../../Images/Icons/GitHub.png")} alt="GitHub Icon"/>
                        GitHub
                    </a>
                </div>
            </div>

        </>
    );
}

export default Footer;
