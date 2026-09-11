import { Link } from "react-router-dom"
import LoginPage from "../authentication/LoginPage"

const HomePage = () => {
  return (
    <div className=" w-full min-h-screen flex justify-center p-3 flex-col">
        <div className="flex font-extrabold text-2xl ">
        AI GROWING WITH YOU
        </div>
        <Link to={"/login"} className="border border-b-gray-950 rounded-md px-2 py-2"/>
        <LoginPage/>
    </div>
  )
}

export default HomePage