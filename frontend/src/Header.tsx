import "./Header.css"
// import { ReactComponent as logoComponent } from './assets/dsa-logo.svg?react';
function Header() {

    return(
        <header className="header">
            {/* <logoComponent /> */}
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