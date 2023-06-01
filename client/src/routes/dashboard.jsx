import { useContext, useState, useEffect } from "react";
import Piechart from "../components/Piechart";
import { AppContext } from "../context";
import Loader from "../components/Loader";
const API_URL = import.meta.env.VITE_API_URL;
export default function Dashboard() {
	const {
		user,
		setUser,
		setToken,
		setIsSignedIn,
		token,
		isLoading,
		setIsLoading,
	} = useContext(AppContext);
	const [records, setRecords] = useState(null);
	useEffect(() => {
		setIsLoading(true);
		const requestOptions = {
			method: "GET",
			headers: {
				Authorization: `Bearer ${token}`,
				"Content-Type": "application/json",
			},
		};
		// using promises to fetch
		const url = `${API_URL}/getRecords`;
		fetch(url, requestOptions)
			.then((response) => response.json())
			.then((data) => {
				setRecords(data);
				setIsLoading(false);
			})
			.catch((error) => console.error(error));
	}, []);
	function increaseSample() {
		const requestOptions = {
			method: "GET",
			headers: {
				Authorization: `Bearer ${token}`,
				"Content-Type": "application/json",
			},
		};
		const url = `${API_URL}/users`;
		fetch(url, requestOptions)
			.then((response) => response.json())
			.then(() => {
				window.location.reload();
			})
			.catch((error) => console.error(error));
	}
	function logout() {
		setUser(null);
		setToken(null);
		setIsSignedIn(false);
		localStorage.removeItem("USER");
		localStorage.removeItem("TOKEN");
	}
	return (
		<>
			<div className="app-container">
				<nav className="navbar">
					<span className="logo">RKA</span>
					<div>
						<span className="name">{user.name}</span>
						<button className="logout" onClick={logout}>
							Logout
						</button>
					</div>
				</nav>
				<div className="content-container">
					<aside className="sidebar">
						<span>DASHBOARD</span>
					</aside>
					{isLoading ? (
						<Loader />
					) : (
						<main>
							<div className="chart-container">
								<div className="chart-header">
									<h1>KEY PERFORMANCE INDICATORS</h1>
									<button onClick={increaseSample}>
										Increase Sample Size
									</button>
								</div>
								{records !== null &&
									Object.entries(records.data).map(
										([key, value]) => (
											<section key={key}>
												<span className="sort-type">
													<h2>{key}</h2>
												</span>
												<span className="sort-chart">
													<Piechart records={value} />
												</span>
												<span className="sort-values">
													<div>
														Total Users ={" "}
														{records.total_records}
													</div>
													<div className="record-values">
														{Object.entries(
															value
														).map(
															([
																subKey,
																subValue,
															]) => (
																<div
																	key={
																		subKey
																	}>
																	{subKey}:{" "}
																	{subValue}
																</div>
															)
														)}
													</div>
												</span>
											</section>
										)
									)}
							</div>
						</main>
					)}
				</div>
			</div>
		</>
	);
}
