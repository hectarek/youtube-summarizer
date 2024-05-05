"use client";

import { SummaryResultsProps } from "@/types";
import { Loader } from "lucide-react";
import { useEffect, useState } from "react";

function SummaryResult({ data }: SummaryResultsProps) {
	const [apiResult, setApiResult] = useState("");
	const [isLoading, setIsLoading] = useState(false);
	const [error, setError] = useState("");

	useEffect(() => {
		if (!data) return;

		const getAPI = async () => {
			setIsLoading(true);
			setError("");

			try {
				
				const res = await fetch("/api/summarize", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({ url: data.values }),
				});

				if (!res.ok) {
					const errorResponse = await res.json();
					console.error(`HTTP error ${res.status}: ${errorResponse}`);
				}

				const responseData = await res.json();
				setApiResult(responseData.response.summary);
			} catch (error) {
				console.error("Error:", error);
				setError("There was an error. Please try again!");
			} finally {
				setIsLoading(false);
			}
		};
		getAPI();
	}, [data]);

	return (
		<section className="flex flex-col">
			<h2 className="text-2xl font-bold pb-6">Generated Summary:</h2>
			{isLoading ? <Loader className="w-8 h-8 animate-spin" /> : error ? <div className="text-red-500">{error}</div> : <div className="max-w-[1280px]" dangerouslySetInnerHTML={{ __html: apiResult }} />}
		</section>
	);
}

export default SummaryResult;
