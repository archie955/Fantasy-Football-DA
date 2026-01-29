import { useNavigate } from "react-router-dom";

function Teams() {

    const navigate = useNavigate()

    const returnToHome = () => {
        navigate('/home')
    }

    return (
        <div>
            <p>This is a teams page for the league</p>
        </div>
    )
    
}

export default Teams