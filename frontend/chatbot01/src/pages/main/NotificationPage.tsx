
import { useNotifications } from "../../context/NotificationContext";

const NotificationPage = () => {
  const {
    notifications,
    unreadCount,
    markAsRead,
    markAllAsRead,
    removeNotification,
  } = useNotifications();

  return (
    <div className="min-h-screen bg-gray-100 px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto w-full max-w-4xl">

        {/* Header */}
        <div className="mb-6 flex flex-col gap-4 rounded-2xl bg-white p-5 shadow-sm sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-800 sm:text-3xl">
              Notifications
            </h1>

            <p className="mt-1 text-sm text-gray-500">
              {unreadCount === 0
                ? "You're all caught up!"
                : `You have ${unreadCount} unread notification${
                    unreadCount === 1 ? "" : "s"
                  }.`}
            </p>
          </div>

          {unreadCount > 0 && (
            <button
              onClick={markAllAsRead}
              className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
            >
              Mark all as read
            </button>
          )}
        </div>

        {/* Notification List */}
        <div className="space-y-3">
          {notifications.length === 0 ? (
            <div className="rounded-2xl bg-white p-10 text-center shadow-sm">
              <div className="mb-4 text-5xl">🔔</div>

              <h2 className="text-lg font-semibold text-gray-800">
                No notifications
              </h2>

              <p className="mt-1 text-sm text-gray-500">
                You're all caught up!
              </p>
            </div>
          ) : (
            notifications.map((notification) => (
              <div
                key={notification.id}
                onClick={() => markAsRead(notification.id)}
                className={`group cursor-pointer rounded-2xl border p-4 transition hover:shadow-md sm:p-5 ${
                  notification.read
                    ? "border-gray-200 bg-white"
                    : "border-blue-200 bg-blue-50"
                }`}
              >
                <div className="flex items-start gap-4">

                  {/* Icon */}
                  <div
                    className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-full text-xl ${
                      notification.read
                        ? "bg-gray-100"
                        : "bg-blue-100"
                    }`}
                  >
                    {notification.type === "course" && "📚"}
                    {notification.type === "message" && "💬"}
                    {notification.type === "system" && "🔔"}
                  </div>

                  {/* Content */}
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                      <h3
                        className={`text-base ${
                          notification.read
                            ? "font-medium text-gray-700"
                            : "font-bold text-gray-900"
                        }`}
                      >
                        {notification.title}
                      </h3>

                      <span className="text-xs text-gray-400">
                        {notification.time}
                      </span>
                    </div>

                    <p className="mt-1 text-sm leading-6 text-gray-600">
                      {notification.message}
                    </p>

                    {!notification.read && (
                      <div className="mt-2 flex items-center gap-2 text-xs font-semibold text-blue-600">
                        <span className="h-2 w-2 rounded-full bg-blue-600" />
                        Unread
                      </div>
                    )}
                  </div>

                  {/* Delete */}
                  <button
                    onClick={(event) => {
                      event.stopPropagation();
                      removeNotification(notification.id);
                    }}
                    className="rounded-lg px-2 py-1 text-gray-400 transition hover:bg-red-50 hover:text-red-500"
                    title="Delete notification"
                  >
                    ✕
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default NotificationPage;

