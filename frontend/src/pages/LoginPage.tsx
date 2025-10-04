import {useState} from "react";

export default function LoginPage(){
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    return (
        <div className="min-h-full grid place-items-center p-6">
            <div className="w-full max-w-md rounded-2xl bg-white shadow p-8">
                <h1 className="text-2xl font-semibold text-gray-900 mb-6">
                    Expense
                </h1>

                <form className="space-y-4" >
                    <div>
                        <label className="block text-sm text-gray-700 mb-1">Email</label>
                        <input type="email" className="w-full rounded-lg border border-gray-300 px-3 py-2 outline-none focus:ring-2 focus: ring-indigo-500"
                            placeholder="......"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)} required minLength={3}
                        />
                    </div>
                    <button type="submit" className="w-full rounded-lg bg-indigo-600 text-white py-2.5 font-medium hover:bgindigo-700 transition">
                        Login / Register
                    </button>
                </form>
                <p className="text-xs text-gray-50 mt-4"></p>
            </div>
        </div>
    )
}