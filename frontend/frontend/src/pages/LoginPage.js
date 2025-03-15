import React from "react";
import Logo from "../assets/LogoWebsite.png";

const handleForgotPassword = () => {
    alert("Chức năng quên mật khẩu đang được phát triển!");
  };
  

const LoginPage = () => {
  return (
    <div className="flex h-screen justify-center items-center">
        {/* Phần trái - Form đăng nhập */}
        <div className="w-full max-w-md flex flex-col justify-center items-center px-8">
            <img src={Logo} alt="Pet Care" className="w-24 mb-4" />
            <h2 className="text-3xl font-bold text-green-500 font-dancing">SmartSprout</h2>
            <p className="text-gray-500 mb-6">Chào mừng bạn đến với SmartSprout</p>

            <form className="w-full">
            <label className="block text-gray-700 font-medium mb-1">Tên đăng nhập</label>
            <input
                type="text"
                placeholder="Nhập tên người dùng"
                className="w-full p-3 border rounded-lg mb-4"
            />

            <label className="block text-gray-700 font-medium mb-1">Mật khẩu</label>
            <input
                type="password"
                placeholder="Nhập mật khẩu"
                className="w-full p-3 border rounded-lg mb-4"
            />

            <div className="flex justify-between items-center text-sm text-gray-500 mb-4">
                <div>
                <input type="checkbox" id="remember" className="mr-1" />
                <label htmlFor="remember">Lưu đăng nhập</label>
                </div>
                <button onClick={handleForgotPassword} className="text-blue-500 hover:underline">
                Quên mật khẩu
                </button>
            </div>

            <button
                type="submit"
                className="w-full py-3 bg-gradient-to-r from-green-500 to-green-700 text-white rounded-lg font-semibold hover:opacity-90 transition"
            >
                Đăng nhập
            </button>
            </form>
        </div>
    </div>

  );
};

export default LoginPage;
