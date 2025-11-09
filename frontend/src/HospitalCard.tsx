import "./HospitalCard.css";

type HospitalCardProps = {
  name: string;
  address: string;
  distance: number;
  functionality: string[];
  onRoute: () => void;
};

function HospitalCard({ name, address, distance, functionality, onRoute }: HospitalCardProps) {
  return (
    <div className="hospital-card">
      <h3 className="hospital-name">{name}</h3>
      <p className="hospital-address">{address}</p>
      <p className="hospital-distance">{distance.toFixed(1)} units away</p>

      <h4>Services / Specialties</h4>
      <ul className="hospital-services">
        {functionality.map((item, idx) => (
          <li key={idx}>{item}</li>
        ))}
      </ul>

      <button className="route-button" onClick={onRoute}>
        Route to this hospital
      </button>
    </div>
  );
}

export default HospitalCard;