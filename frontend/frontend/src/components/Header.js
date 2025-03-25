import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode"; // ✅ Import đúng
import Logo from "../assets/LogoWebsite.png";

const Header = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [userName, setUserName] = useState(""); // 👈 State lưu tên người dùng
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        if (token) {
            try {
                const decoded = jwtDecode(token);
                const fullName = `${decoded.last_name} ${decoded.first_name}`;
                setUserName(fullName);
            } catch (err) {
                console.error("Token không hợp lệ:", err);
            }
        }
    }, []);

    return (
        <div className="h-[100px] bg-gray-100">
            <div className="flex items-center justify-between px-6">
                {/* Logo + Tên */}
                <div className="flex items-center space-x-2">
                    <img src={Logo} alt="Logo" className="w-[100px]" />
                    <span className="text-xl text-green-500 mt-2 font-dancing">SmartSprout</span>
                </div>

                {/* Avatar + Dropdown */}
                <div className="relative">
                    <button
                        onClick={() => setIsOpen(!isOpen)}
                        className="flex items-center space-x-2 focus:outline-none"
                    >
                        <img src={Logo} alt="User Avatar" className="w-10 h-10 rounded-full border border-gray-300" />
                        <span className="text-gray-700 font-medium">{userName || "Người dùng"}</span>
                    </button>

                    {/* Dropdown menu */}
                    {isOpen && (
                        <div className="absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-lg">
                            <ul className="py-2">
                                <li 
                                    className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                                    onClick={() => navigate("/account-settings")} // Điều hướng đến trang cài đặt tài khoản
                                >
                                    Cài đặt tài khoản
                                </li>
                                <li 
                                    className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                                    onClick={() => {
                                        localStorage.removeItem("access_token");
                                        localStorage.removeItem("refresh_token");
                                        navigate("/")
                                    }} 
                                >
                                    Đăng xuất
                                </li>
                            </ul>
                        </div>
                    )}
                </div>
            </div>

            {/* Đường kẻ dưới */}
            <div className="h-[6px] bg-gradient-to-b from-gray-300 to-gray-100 w-full"></div>
        </div>
    );
};

export default Header;
