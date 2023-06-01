import { useState, useRef, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AppContext } from "../context";
import Loader from "../components/Loader";
const API_URL = import.meta.env.VITE_API_URL;
export default function Login() {
	const {
		setUser,
		setIsSignedIn,
		isSignedIn,
		setToken,
		isLoading,
		setIsLoading,
	} = useContext(AppContext);
	const navigate = useNavigate();
	const [onLoginPage, setOnLoginPage] = useState(true);
	const [error, setError] = useState(null);
	const nameRef = useRef();
	const emailRef = useRef();
	const passwordRef = useRef();
	useEffect(() => {
		if (isSignedIn) {
			navigate("/dashboard");
		}
	}, []);
	async function login(e) {
		setIsLoading(true);
		setError(null);
		e.preventDefault();
		if (!emailRef.current.value || !passwordRef.current.value) return;
		const data = {
			email: emailRef.current.value,
			password: passwordRef.current.value,
		};
		const response = await postData("login", data);
		const response_json = await response.json();
		if (response.status === 200) {
			setUser(response_json.user);
			setIsSignedIn(true);
			setToken(response_json.token);
			localStorage.setItem("TOKEN", response_json.token);
			localStorage.setItem("USER", JSON.stringify(response_json.user));
			navigate("/dashboard");
		}
		setError(response_json.message);
		setIsLoading(false);
	}
	async function register(e) {
		setIsLoading(true);
		setError(null);

		e.preventDefault();
		if (
			!nameRef.current.value ||
			!emailRef.current.value ||
			!passwordRef.current.value
		)
			return;
		const data = {
			email: emailRef.current.value,
			name: nameRef.current.value,
			password: passwordRef.current.value,
		};
		const response = await postData("register", data);
		if (response.status === 200) {
			login(e);
		}
		const response_json = await response.json();
		setError(response_json.message);
		setIsLoading(false);
	}

	async function postData(endpoint, data) {
		const requestOptions = {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		};
		// using async await to fetch
		const response = await fetch(`${API_URL}/${endpoint}`, requestOptions);
		return response;
	}
	return (
		<form className="login-container">
			<div className="login-card">
				<h1 className="heading">
					{onLoginPage ? "Login" : "Register"}
				</h1>
				{error !== null && <div className="error">{error}</div>}
				{!onLoginPage && (
					<input type="text" placeholder="Username" ref={nameRef} />
				)}

				<input type="email" placeholder="Email" ref={emailRef} />
				<input
					type="password"
					placeholder="Password"
					ref={passwordRef}
				/>
				{onLoginPage ? (
					<button className="login-btn" onClick={(e) => login(e)}>
						{isLoading ? <Loader /> : "Login"}
					</button>
				) : (
					<button className="login-btn" onClick={(e) => register(e)}>
						{isLoading ? <Loader /> : "Register"}
					</button>
				)}
				{onLoginPage ? (
					<p>
						Don't have an account ?{" "}
						<span onClick={() => setOnLoginPage((prev) => !prev)}>
							Register Now
						</span>
					</p>
				) : (
					<p>
						Already have an account ?{" "}
						<span onClick={() => setOnLoginPage((prev) => !prev)}>
							Login
						</span>
					</p>
				)}
			</div>
			<a
				className="github-logo"
				href="https://github.com/MaahiVohra/record-keeping-application"
				target="_blank">
				<svg
					height="32"
					aria-hidden="true"
					viewBox="0 0 16 16"
					version="1.1"
					width="32"
					data-view-component="true"
					className="octicon octicon-mark-github v-align-middle">
					<path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path>
				</svg>
			</a>
		</form>
	);
}
