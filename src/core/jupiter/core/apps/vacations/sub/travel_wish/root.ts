import type { TravelWish } from "@jupiter/webapi-client";

export function sortTravelWishesNaturally(travelWishes: TravelWish[]) {
  return [...travelWishes].sort((w1, w2) => {
    if (w1.name === w2.name) {
      return 0;
    }
    return w1.name < w2.name ? -1 : 1;
  });
}
