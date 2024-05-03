"use client";

import { SummaryResultsProps } from "@/types";
import { Loader } from "lucide-react";
import { useEffect, useState } from "react";

function SummaryResult({ data }: SummaryResultsProps) {
	const [apiResult, setApiResult] = useState("");
    const [isLoading, setIsLoading] = useState(false);

	useEffect(() => {

        if (!data) return;

		const getAPI = async () => {
            setIsLoading(true); 

			try {
				const res = await fetch("http://localhost:8080/api/summarize", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
                    credentials: 'include',
					body: JSON.stringify({ url: data.values}),
				});

                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }

				const responseData = await res.json();
				console.log("Success:", responseData);
				setApiResult(responseData.summary);
			} catch (error) {
				console.error("Error:", error);
			} finally {
                setIsLoading(false);
            }
		};
		getAPI();
	}, [data]);

	return (
		<section className="flex flex-col">
			<h2 className="text-2xl font-bold pb-6">Generated Summary:</h2>
            {isLoading ? <Loader className="w-8 h-8 animate-spin"/> : <div className="max-w-[1280px]" dangerouslySetInnerHTML={{ __html: apiResult }} />}
		</section>
	);
}

export default SummaryResult;
