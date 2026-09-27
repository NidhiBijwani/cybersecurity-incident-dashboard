import { useState } from "react";
import api from "../services/api";

function Login() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    async function handleLogin(e) {

        e.preventDefault();

        try {

            const body = new URLSearchParams();

            body.append("username", username);
            body.append("password", password);

            const response = await api.post(
                "/login",
                body
            );

            console.log("LOGIN RESPONSE:", response.data);

            localStorage.setItem(
                "token",
                response.data.access_token
            );

            window.location.href = "/dashboard";

        } catch (error) {

            console.log("LOGIN ERROR:", error);
            console.log("STATUS:", error.response?.status);
            console.log("DATA:", error.response?.data);

            setMessage(
                error.response?.data?.detail ||
                "Login request failed"
            );
        }
    }

    return (
        <div>

            <h1>AI Cybersecurity Incident Dashboard</h1>

            <form onSubmit={handleLogin}>

                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) =>
                        setUsername(e.target.value)
                    }
                />

                <br /><br />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) =>
                        setPassword(e.target.value)
                    }
                />

                <br /><br />

                <button type="submit">
                    Login
                </button>

            </form>

            <p>{message}</p>

        </div>
    );
}

export default Login;