from fastapi import FastAPI, BackgroundTasks
from time import sleep

app = FastAPI()


def make_order(customer_name: str):
    print(f"☕ [START] Brewing coffee for {customer_name}...")
    sleep(5)  # Simulates a slow, heavy task
    print(f"✅ [DONE] Coffee ready for {customer_name}!")


@app.get("order/{name}")
def background_helper(name: str, bg: BackgroundTasks):
    bg.add_task(make_order, customer_name=name)

    return {
        "message": f"{name} your order is ready!!!"
    }


# if __name__ == "__main__":
#     background_helper
