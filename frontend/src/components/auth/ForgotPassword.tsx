import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { Button, Input } from "../common";
import axios from "axios";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post(
        `${
          import.meta.env.VITE_API_URL || "http://localhost:8000"
        }/auth/forgot-password`,
        { email }
      );
      toast.success("If the email exists, an OTP has been sent");
      navigate("/reset-password", { state: { email } });
    } catch (e: any) {
      toast.success("If the email exists, an OTP has been sent"); // still generic
      navigate("/reset-password", { state: { email } });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden border border-gray-200 p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          Forgot Password
        </h2>
        <p className="text-sm text-gray-600 mb-6 text-center">
          Enter your registered email to receive a one-time password (OTP).
        </p>
        <form onSubmit={handleSubmit} className="space-y-6">
          <Input
            label="Email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
          />
          <Button
            type="submit"
            variant="primary"
            loading={loading}
            className="w-full"
          >
            Send OTP
          </Button>
        </form>
        <div className="mt-6 text-center">
          <button
            onClick={() => navigate("/login")}
            className="text-sm text-blue-600 hover:underline"
          >
            Back to Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
