import {useState} from "react";
import {login, register, Role} from "../lib/api";

export default function LoginPage(){
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [step, setStep] = useState<"login" | "register">("login");
    const [error, setError] = useState<string | null>(null);

    const [role, setRole] = useState<Role>("EMPLOYEE");
    const [username, setUsername] = useState("");

    async  function handleSubmit(e: React.FormEvent){
        e.preventDefault();
        setError(null);
        if (step === "login"){
            try{
                const res = await login(email, password);
                alert("Login sucess");
            }catch (err: any){
                if(err?.status === 403){
                    setError("You account is suspended");
                    return;
                }
                setStep("register");
                setError("未找到账户或密码错误")
            }
        }else {
            if (!username.trim()){
                setError("请填写用户名")；
                return;
            }
            try {
                const  res = await register(email, password, role);
                alert("注册并登录成功")；
            }catch (err: any){
                if (err?.status === 400){
                    setError("邮箱已存在，请返回登录并使用正确密码")；
                    setStep("login");
                }else {
                    setError(err?.detail ?? "注册失败")
                }
            }
        }
    }
    return (
        <div className="min-h-full grid place-items-center p-6">
            <div className="w-full max-w-md rounded-2xl bg-white shadow p-8">
                <h1 className="text-2xl font-semibold text-gray-900 mb-6">
                    Expense
                </h1>
                <p className="text-sm text-gray-500 mb-6">
                    使用公司邮箱登录；如不存在，我们会引导你注册。
                </p>

                <form className="space-y-4" onSubmit={handleSubmit}>//开始做检查
                    <div>
                        <label className="block text-sm text-gray-700 mb-1">Email</label>
                        <input type="email" className="w-full rounded-lg border border-gray-300 px-3 py-2 outline-none focus:ring-2 focus: ring-indigo-500"
                            placeholder="12345678@qq.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value.trim)} required
                        />
                    </div>

                    <div>
                        //独占一行，文字small(14px),margin-bottom: 0.25rem（即大约 4px）
                        <label className="block text-sm text-gray-700 mb-1">Password</label>
                        <input
                            type="password"
                            //宽度占满父容器,px-3左右内边距，py-2上下内边距，focus:ring-2（box-shadow样式），样式颜色
                            className="w-full rounded-lg border-gray-300 px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            //需要设定密码组合类型
                            minLength={3}
                        />
                    </div>
                    {step === "register" && (
                        <div className="space-y-3 border-t pt-4">
                            <div>
                                <label className="block text-sm text-gray-700 mb-1">Role</label>
                                <div className="flex gap-3">
                                    <label className="inline-flex items-center gap-2">
                                        <input
                                            type="radio"
                                            name="role"
                                            value="EMPLOYEE"
                                            checked={role === "EMPLOYEE"}
                                            onChange={() => setRole("EMPLOYEE")}
                                        />
                                        <span>Employee</span>
                                    </label>
                                    <label className="inline-flex items-center gap-2">
                                        <input
                                            type="radio"
                                            name="role"
                                            value="EMPLOYER"
                                            checked={role === "EMPLOYER"}
                                            onChange={() => setRole("EMPLOYER")}
                                        />
                                        <span>Employer</span>
                                    </label>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm text-gray-700 mb-1">Username</label>
                                <input
                                    className="w-full rounded-lg border border-gray-300 px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500"
                                    placeholder="Your display name"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                />
                                <p className="text-xs text-gray-500 mt-1">
                                    仅用于前端显示，不会保存到后端数据库
                                </p>
                            </div>
                        </div>
                    )}
                    <button type="submit" className="w-full rounded-lg bg-indigo-600 text-white py-2.5 font-medium hover:bgindigo-700 transition">
                        Login / Register
                    </button>
                </form>
                <p className="text-xs text-gray-50 mt-4"></p>
            </div>
        </div>
    )
}