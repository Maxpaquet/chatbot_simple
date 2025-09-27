import { useEffect, useState } from 'react'


export default function Home() {
    const [items, setItems] = useState([])
    const [name, setName] = useState('')
    const [notification, setNotification] = useState('')


    // Use Next.js API route as proxy
    // const apiUrl = "/api"
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"


    useEffect(() => {
        fetch(`${apiUrl}/items`)
            .then(r => r.json())
            .then(setItems)
            .catch(console.error)
    }, [])


    async function addItem(e) {
        console.log('addItem called')
        e.preventDefault()
        const newItem = { id: Date.now(), name, description: '' }
        try {
            const res = await fetch(`${apiUrl}/items`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newItem)
            })
            if (!res.ok) {
                const errorText = await res.text()
                console.error('POST /items failed:', res.status, errorText)
                setNotification('Error: Could not add element!')
                setTimeout(() => setNotification(''), 3000)
                return
            }
            const data = await res.json()
            setItems(prev => [...prev, data])
            setName('')
            setNotification('Element added to the database!')
            setTimeout(() => setNotification(''), 2000)
        } catch (err) {
            console.error('Network or JS error:', err)
            setNotification('Error: Could not reach backend!')
            setTimeout(() => setNotification(''), 3000)
        }
    }


    return (
        <main style={{ padding: 20 }}>
            <div style={{ background: 'yellow', padding: '10px', marginBottom: '10px' }}>TEST DIV: If you see this, index.js is active</div>
            <h1>Next.js + FastAPI</h1>
            {notification && (
                <div style={{ background: '#d4edda', color: '#155724', padding: '10px', marginBottom: '10px', borderRadius: '4px' }}>
                    {notification}
                </div>
            )}
            <form onSubmit={addItem}>
                <input value={name} onChange={e => setName(e.target.value)} placeholder="Name" />
                <button type="submit">Add</button>
            </form>
            <ul>
                {items.map(i => (
                    <li key={i.id}>{i.name} (id: {i.id})</li>
                ))}
            </ul>
        </main>
    )
}