import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import React from "react";

const MetricCard = ({
  title,
  value,
  icon,
  isLoading = false,
  onClick,
}: {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  isLoading?: boolean;
  onClick?: () => void;
}) => {
  const isClickable = Boolean(onClick);

  return (
    <Card
      onClick={onClick}
      role={isClickable ? "button" : undefined}
      tabIndex={isClickable ? 0 : undefined}
      onKeyDown={
        isClickable
          ? (event) => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                onClick?.();
              }
            }
          : undefined
      }
      className={`shadow-sm border-slate-200 ${
        isClickable
          ? "cursor-pointer transition-shadow hover:shadow-md focus-visible:ring-2 focus-visible:ring-slate-400 focus-visible:outline-none"
          : ""
      }`}
    >
      <CardContent className="p-6 flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500 mb-1">{title}</p>
          {isLoading ? (
            <Skeleton className="h-9 w-20" />
          ) : (
            <h3 className="text-3xl font-bold text-slate-800">{value}</h3>
          )}
        </div>
        <div className="p-3 bg-slate-100 rounded-full">{icon}</div>
      </CardContent>
    </Card>
  );
};

export default MetricCard;
