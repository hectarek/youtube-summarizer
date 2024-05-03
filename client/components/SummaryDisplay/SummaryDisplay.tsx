"use client";

import { useState } from "react";
import { SummaryForm } from "../SummaryForm/SummaryForm";
import SummaryResult from "../SummaryResult/SummaryResult";

function SummaryDisplay() {
	const [summaryData, setSummaryData] = useState(null);

	return (
		<section className="md:container md:mx-auto space-y-10">
			<SummaryForm setSummaryData={setSummaryData} />
			{summaryData && <SummaryResult data={summaryData} />}
		</section>
	);
}

export default SummaryDisplay;
