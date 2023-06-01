import React, { useState, useContext } from "react";
import Login from "./routes/login.jsx";
import Dashboard from "./routes/dashboard.jsx";
import ErrorPage from "./error-page.jsx";
import Protected from "./protected.jsx";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { AppContext } from "./context.jsx";
export default function App() {
	const { isSignedIn } = useContext(AppContext);
	const router = createBrowserRouter([
		{
			path: "/",
			element: <Login />,
			errorElement: <ErrorPage />,
		},
		{
			path: "/dashboard",
			element: (
				<Protected isSignedIn={isSignedIn}>
					<Dashboard />
				</Protected>
			),
		},
	]);
	return <RouterProvider router={router} />;
}
