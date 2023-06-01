import React, { createContext, useState } from "react";

export const AppContext = createContext();

export function AppContextProvider({ children }) {
	const [user, setUser] = useState(localStorage.getItem("USER") || null);
	const [token, setToken] = useState(localStorage.getItem("TOKEN") || null);
	const [isSignedIn, setIsSignedIn] = useState(token ? true : false);

	const value = {
		user: user,
		setUser: setUser,
		isSignedIn: isSignedIn,
		setIsSignedIn: setIsSignedIn,
		token: token,
		setToken: setToken,
	};

	return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}
