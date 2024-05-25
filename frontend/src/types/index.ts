export interface User {
  id: number;
  name: string;
  email: string;
  role: "user" | "admin";
}

export interface VerificationRequest {
  id: number;
  userId: number;
  status: "pending" | "approved" | "rejected";
  createdAt: string;
  updatedAt: string;
}

export interface APIKey {
  id: string;
  name: string;
  key: string;
  createdAt: string;
}

export interface BillingData {
  currentPlan: string;
  nextBillingDate: string;
  paymentMethod: string;
  billingHistory: BillingHistoryItem[];
}

export interface BillingHistoryItem {
  id: string;
  amount: number;
  date: string;
  status: "paid" | "pending" | "failed";
}

export interface UserSettings {
  name: string;
  email: string;
  phoneNumber: string;
  twoFactorAuth: boolean;
}
