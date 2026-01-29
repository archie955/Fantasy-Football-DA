import { useNavigate } from "react-router-dom";

function Leagues() {

    const navigate = useNavigate()

    const returnToHome = () => {
        navigate('/home')
    }

    
}

export default Leagues