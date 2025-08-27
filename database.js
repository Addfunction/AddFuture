
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export async function getServerSideProps() {
  const examples = await prisma.example.findMany()
  return {
    props: { examples },
  }
}

export default function DatabasePage({ examples }) {
  return (
    <div className="min-h-screen bg-gray-100 p-10">
      <h1 className="text-3xl font-bold mb-6">Databaseinnhold</h1>
      <ul className="space-y-4">
        {examples.map((item) => (
          <li key={item.id} className="bg-white p-4 rounded shadow">
            <p><strong>Navn:</strong> {item.name}</p>
            <p><strong>E-post:</strong> {item.email}</p>
          </li>
        ))}
      </ul>
    </div>
  )
}
