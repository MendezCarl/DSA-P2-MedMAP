import "./HospitalCard.css";

function HospitalCard() { 
    return( 
        <div className="hospital-card">
            <img></img>
            <p>Hospital Name</p>
            <ul>Specialties 
                <li>Specialty 1</li>
                <li>Specialty 2</li>
                <li>Specialty 3</li>
            </ul>
            
        </div>
    );
}

export default HospitalCard;