import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "../assets/LogoWebsite.png";

const RegisterPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    fullname: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert("Mật khẩu xác nhận không khớp!");
      return;
    }
    console.log("Đăng ký thành công:", formData);
    navigate("/login"); // Chuyển hướng đến trang đăng nhập sau khi đăng ký
  };

  return (
    <div className="flex h-screen justify-center items-center">
      {/* Phần Form đăng ký */}
      <div className="w-full md:w-1/2 flex flex-col justify-center items-center px-6 md:px-16">
        <img src={Logo} alt="SmartSprout" className="w-24 mb-4" />
        <h2 className="text-3xl font-bold text-green-500 font-dancing">SmartSprout</h2>
        <p className="text-gray-500 mb-6">Tạo tài khoản mới để bắt đầu</p>

        <form className="w-full max-w-md" onSubmit={handleSubmit}>
          <label className="block text-gray-700 font-medium mb-1">Họ và tên</label>
          <input
            type="text"
            name="fullname"
            placeholder="Nhập họ tên của bạn"
            className="w-full p-3 border rounded-lg mb-4"
            value={formData.fullname}
            onChange={handleChange}
            required
          />

          <label className="block text-gray-700 font-medium mb-1">Email</label>
          <input
            type="email"
            name="email"
            placeholder="Nhập email"
            className="w-full p-3 border rounded-lg mb-4"
            value={formData.email}
            onChange={handleChange}
            required
          />

          <label className="block text-gray-700 font-medium mb-1">Mật khẩu</label>
          <input
            type="password"
            name="password"
            placeholder="Nhập mật khẩu"
            className="w-full p-3 border rounded-lg mb-4"
            value={formData.password}
            onChange={handleChange}
            required
          />

          <label className="block text-gray-700 font-medium mb-1">Xác nhận mật khẩu</label>
          <input
            type="password"
            name="confirmPassword"
            placeholder="Nhập lại mật khẩu"
            className="w-full p-3 border rounded-lg mb-4"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />

          <button
            type="submit"
            className="w-full py-3 bg-gradient-to-r from-green-500 to-green-700 text-white rounded-lg font-semibold hover:opacity-90 transition"
          >
            Đăng ký
          </button>
        </form>

        <p className="mt-4 text-gray-600 text-sm">
          Đã có tài khoản?{" "}
          <button onClick={() => navigate("/login")} className="text-green-500 hover:underline">
            Đăng nhập ngay
          </button>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
