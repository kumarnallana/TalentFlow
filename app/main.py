from fastapi import FastAPI, BackgroundTasks
from time import sleep

app = FastAPI()


def make_order(customer_name: str):
    print(f"☕ [START] Brewing coffee for {customer_name}...")
    sleep(5)  # Simulates a slow, heavy task
    print(f"✅ [DONE] Coffee ready for {customer_name}!")


@app.post("/order/{name}")
def normal_helper(name: str):
    make_order(name)  # Client is blocked here for 5 full seconds
    return {"message": "done"}


# if __name__ == "__main__":
#     background_helper
