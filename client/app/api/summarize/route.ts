import { NextResponse } from "next/server"

export async function POST(request: Request) {
    const res = await new NextResponse(request.body).json()
    const apiUrl = process.env.SERVER_URL;

    try {
        const postResponse = await fetch(`${apiUrl}/api/summarize`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({ url: res.url }),
        });

        if (!postResponse.ok) {
            const errorResponse = await res.json();
            console.error(`HTTP error ${res.status}: ${errorResponse}`);
        }

        const summaryData = await postResponse.json();

        return NextResponse.json({
            statusCode: 200,
            response: summaryData,
        })

    } catch (error: any) {
        NextResponse.json({
            statusCode: error.statusCode || 500,
            message: error.message,
        })
        throw new Error("Error hitting api:", error)
    }
}