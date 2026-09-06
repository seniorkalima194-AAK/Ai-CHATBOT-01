
import {
  createContext,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";

export interface Notification {
  id: number;
  title: string;
  message: string;
  time: string;
  type: "course" | "message" | "system";
  read: boolean;
}

interface NotificationContextType {
  notifications: Notification[];
  unreadCount: number;
  markAsRead: (id: number) => void;
  markAllAsRead: () => void;
  removeNotification: (id: number) => void;
  addNotification: (notification: Notification) => void;
}

const NotificationContext =
  createContext<NotificationContextType | undefined>(undefined);

const initialNotifications: Notification[] = [
  {
    id: 1,
    title: "New Course Available",
    message: "A new React course has been added.",
    time: "5 min ago",
    type: "course",
    read: false,
  },
  {
    id: 2,
    title: "New Message",
    message: "You have received a new message.",
    time: "20 min ago",
    type: "message",
    read: false,
  },
  {
    id: 3,
    title: "System Update",
    message: "Your account has been successfully updated.",
    time: "1 hour ago",
    type: "system",
    read: false,
  },
];

export const NotificationProvider = ({
  children,
}: {
  children: ReactNode;
}) => {
  const [notifications, setNotifications] =
    useState<Notification[]>(initialNotifications);

  const unreadCount = useMemo(
    () => notifications.filter((notification) => !notification.read).length,
    [notifications]
  );

  const markAsRead = (id: number) => {
    setNotifications((current) =>
      current.map((notification) =>
        notification.id === id
          ? { ...notification, read: true }
          : notification
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications((current) =>
      current.map((notification) => ({
        ...notification,
        read: true,
      }))
    );
  };

  const removeNotification = (id: number) => {
    setNotifications((current) =>
      current.filter((notification) => notification.id !== id)
    );
  };

  const addNotification = (notification: Notification) => {
    setNotifications((current) => [notification, ...current]);
  };

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        unreadCount,
        markAsRead,
        markAllAsRead,
        removeNotification,
        addNotification,
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
};

export const useNotifications = () => {
  const context = useContext(NotificationContext);

  if (!context) {
    throw new Error(
      "useNotifications must be used inside NotificationProvider"
    );
  }

  return context;
};

