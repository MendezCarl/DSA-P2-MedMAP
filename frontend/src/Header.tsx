import "./Header.css"
function Header() {

    return(
        <header className="header">
            <nav className="navbar">
                <div id="logo">MedMap </div>
                <div>
                    <a href="#" >About</a>
                    <a href="#" >Account</a>
                    <a href="#">Browse</a>
                </div>
            </nav>
        </header>

    );
}

export default Header;