import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Analytics from "./pages/Analytics";
import ProtectedRoute from "./components/ProtectedRoute";


function App() {

    return (

        <BrowserRouter>

            <Routes>

                {/* Login */}

                <Route
                    path="/"
                    element={<Login />}
                />


                {/* Protected Dashboard */}

                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />


                {/* Protected Analytics */}

                <Route
                    path="/analytics"
                    element={
                        <ProtectedRoute>
                            <Analytics />
                        </ProtectedRoute>
                    }
                />

            </Routes>

        </BrowserRouter>
    );
}


export default App;