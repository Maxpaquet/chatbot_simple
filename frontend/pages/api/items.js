// Next.js API route to proxy requests to the FastAPI backend
export default async function handler(req, res) {
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || "http://backend:8000";
    const url = `${backendUrl}/items`;

    if (req.method === 'GET') {
        const response = await fetch(url);
        const data = await response.json();
        res.status(response.status).json(data);
    } else if (req.method === 'POST') {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(req.body)
        });
        const data = await response.json();
        res.status(response.status).json(data);
    } else {
        res.setHeader('Allow', ['GET', 'POST']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}
