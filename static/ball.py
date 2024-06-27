from vpython import *
import random

# Membuat kanvas untuk simulasi VPython dengan ukuran 800x600 piksel dan pusat di (0,0,0)
scene = canvas(title='Tugas Lima Bola Memantul Menggunakan Keyboard dan MODE BERHENTI TEKAN T', width=800, height=600, center=vector(0,0,0))

# Warna-warna yang telah ditentukan untuk bola-bola
colors = [vector(1, 0, 0),  # Merah
          vector(0, 0, 1),  # Biru
          vector(0, 1, 0),  # Hijau
          vector(0.5, 0.5, 0.5),  # Abu-abu
          vector(1, 0.5, 0),  # Oranye
          vector(1, 0, 1)]  # Ungu (digerakkan oleh keyboard)

# Fungsi untuk menghasilkan kecepatan acak untuk bola
def random_velocity():
    # Menghasilkan kecepatan acak dalam kisaran -1 hingga 1 untuk sumbu x dan y
    return vector(random.uniform(-1, 1), random.uniform(-1, 1), 0)

# Membuat bola-bola dengan posisi acak dan kecepatan acak
balls = []
for i in range(6):
    ball = sphere(pos=vector(random.uniform(-4.5, 4.5), random.uniform(-4.5, 4.5), 0),
                  radius=0.5,
                  color=colors[i])
    ball.velocity = random_velocity()
    balls.append(ball)

# Menandai bola ungu yang akan digerakkan oleh keyboard
purple_ball = balls[5]

# Membuat kotak bingkai (frame) dengan ukuran tertentu
frame_size = 5
box_bottom = box(pos=vector(0, -frame_size, 0), size=vector(10, 0.1, 10), color=color.white)
box_top = box(pos=vector(0, frame_size, 0), size=vector(10, 0.1, 10), color=color.white)
box_left = box(pos=vector(-frame_size, 0, 0), size=vector(0.1, 10, 10), color=color.white)
box_right = box(pos=vector(frame_size, 0, 0), size=vector(0.1, 10, 10), color=color.white)

# Label untuk menampilkan jumlah tabrakan
collision_text = label(pos=vector(0, frame_size + 1, 0), text='Collisions: 0', height=20, color=color.white, box=False)

# Variabel untuk menyimpan jumlah tabrakan
collision_count = 0

# Interval waktu untuk pembaruan posisi bola dan kecepatan pergerakan bola ungu
dt = 0.01
kecepatan = 0.1

# Status pencapaian
achievement_status = ""

# Pilihan untuk bola-bola berhenti atau memantul saat bertabrakan
stop_on_collision = False

# Fungsi untuk menggerakkan bola ungu berdasarkan input keyboard
def move_purple_ball(evt):
    global collision_count, achievement_status, stop_on_collision
    
    # Menggerakkan bola ungu sesuai dengan tombol yang ditekan (atas, bawah, kiri, kanan)
    if evt.key == 'up' and purple_ball.pos.y + purple_ball.radius + kecepatan <= frame_size:
        purple_ball.pos.y += kecepatan
    elif evt.key == 'down' and purple_ball.pos.y - purple_ball.radius - kecepatan >= -frame_size:
        purple_ball.pos.y -= kecepatan
    elif evt.key == 'left' and purple_ball.pos.x - purple_ball.radius - kecepatan >= -frame_size:
        purple_ball.pos.x -= kecepatan
    elif evt.key == 'right' and purple_ball.pos.x + purple_ball.radius + kecepatan <= frame_size:
        purple_ball.pos.x += kecepatan
    elif evt.key == 't':
        stop_on_collision = not stop_on_collision  # Toggle berhenti atau tidak saat bertabrakan

    # Mengecek tabrakan antara bola ungu dan bola lainnya
    for ball in balls:
        if ball != purple_ball:
            distance = mag(purple_ball.pos - ball.pos)  # Menghitung jarak antara bola ungu dan bola lainnya
            if distance <= purple_ball.radius + ball.radius:  # Jika jarak kurang dari atau sama dengan total radius kedua bola
                collision_count += 1
                collision_text.text = f'Collisions: {collision_count}'

                v1 = purple_ball.velocity
                v2 = ball.velocity
                m1 = m2 = 1  # Massa bola diatur sama

                direction = norm(purple_ball.pos - ball.pos)  # Menghitung arah dari bola ungu ke bola lainnya

                # Komponen kecepatan sejajar dan tegak lurus arah tabrakan
                v1_parallel = dot(v1, direction) * direction
                v1_perpendicular = v1 - v1_parallel
                v2_parallel = dot(v2, direction) * direction
                v2_perpendicular = v2 - v2_parallel

                # Menghentikan bola yang bertabrakan jika opsi stop_on_collision diaktifkan
                if stop_on_collision:
                    ball.velocity = vector(0, 0, 0)
                else:
                    # Menukar komponen kecepatan sejajar
                    purple_ball.velocity = v2_parallel + v1_perpendicular
                    ball.velocity = v1_parallel + v2_perpendicular

                # Memberikan pencapaian berdasarkan jumlah tabrakan
                if collision_count == 50:
                    achievement_status = "Warrior!"
                elif collision_count == 100:
                    achievement_status = "Elite!"
                elif collision_count == 150:
                    achievement_status = "Master!"
                elif collision_count == 200:
                    achievement_status = "Grandmaster!"

                return
    collision_text.text = f'Collisions: {collision_count}'

# Mengikat fungsi move_purple_ball dengan event keydown
scene.bind('keydown', move_purple_ball)

# Label untuk menampilkan pencapaian
achievement_text = label(pos=vector(0, frame_size + 2, 0), text='', height=20, color=color.yellow, box=False)

# Label untuk menampilkan waktu yang tersisa
timer_text = label(pos=vector(0, frame_size + 3, 0), text='Time Left: 60s', height=20, color=color.white, box=False)

# Fungsi untuk menjalankan simulasi
def vpython_simulation():
    global collision_count, achievement_status, stop_on_collision
    start_time = clock()  # Mencatat waktu mulai simulasi
    while True:
        elapsed_time = clock() - start_time  # Menghitung waktu yang telah berlalu
        time_left = 60 - int(elapsed_time)  # Menghitung waktu yang tersisa
        
        if time_left <= 0:
            break  # Menghentikan simulasi jika waktu habis
        
        timer_text.text = f'Time Left: {time_left}s'  # Memperbarui label waktu yang tersisa
        
        rate(200)  # Mengatur kecepatan loop
        
        # Memperbarui posisi bola
        for ball in balls:
            if ball != purple_ball:
                ball.pos += ball.velocity * dt  # Memperbarui posisi bola berdasarkan kecepatan dan interval waktu

                # Mengatur pantulan bola ketika menyentuh batas frame
                if ball.pos.x - ball.radius < -frame_size:
                    ball.pos.x = -frame_size + ball.radius
                    ball.velocity.x *= -1
                elif ball.pos.x + ball.radius > frame_size:
                    ball.pos.x = frame_size - ball.radius
                    ball.velocity.x *= -1
                
                if ball.pos.y - ball.radius < -frame_size:
                    ball.pos.y = -frame_size + ball.radius
                    ball.velocity.y *= -1
                elif ball.pos.y + ball.radius > frame_size:
                    ball.pos.y = frame_size - ball.radius
                    ball.velocity.y *= -1

            # Mengatur batas gerak bola ungu
            if purple_ball.pos.x - purple_ball.radius < -frame_size:
                purple_ball.pos.x = -frame_size + purple_ball.radius
            elif purple_ball.pos.x + purple_ball.radius > frame_size:
                purple_ball.pos.x = frame_size - purple_ball.radius
            
            if purple_ball.pos.y - purple_ball.radius < -frame_size:
                purple_ball.pos.y = -frame_size + purple_ball.radius
            elif purple_ball.pos.y + purple_ball.radius > frame_size:
                purple_ball.pos.y = frame_size - purple_ball.radius
            
            # Mengecek tabrakan antara bola-bola lainnya
            for other_ball in balls:
                if other_ball != ball:
                    distance = mag(ball.pos - other_ball.pos)
                    if distance <= ball.radius + other_ball.radius:
                        overlap = ball.radius + other_ball.radius - distance  # Menghitung overlap antara bola
                        direction = norm(ball.pos - other_ball.pos)  # Menghitung arah tabrakan
                        ball.pos += direction * overlap / 2  # Menyesuaikan posisi bola untuk mengurangi overlap
                        other_ball.pos -= direction * overlap / 2

                        v1 = ball.velocity
                        v2 = other_ball.velocity
                        m1 = m2 = 1  # Massa bola diatur sama

                        if stop_on_collision and (ball == purple_ball or other_ball == purple_ball):
                            # Menghentikan bola yang bertabrakan dengan bola ungu jika opsi stop_on_collision diaktifkan
                            ball.velocity = vector(0, 0, 0)
                            other_ball.velocity = vector(0, 0, 0)
                        else:
                            # Menghitung kecepatan baru setelah tabrakan
                            ball.velocity = v1 - 2 * m2 / (m1 + m2) * dot(v1 - v2, ball.pos - other_ball.pos) / mag(ball.pos - other_ball.pos)**2 * (ball.pos - other_ball.pos)
                            other_ball.velocity = v2 - 2 * m1 / (m1 + m2) * dot(v2 - v1, other_ball.pos - ball.pos) / mag(other_ball.pos - ball.pos)**2 * (other_ball.pos - ball.pos)

    # Setelah waktu habis, memberikan pencapaian berdasarkan jumlah tabrakan
    if collision_count >= 200:
        achievement_status = "Grandmaster!"
    elif collision_count >= 150:
        achievement_status = "Master!"
    elif collision_count >= 100:
        achievement_status = "Elite!"
    elif collision_count >= 50:
        achievement_status = "Warrior!"
    else:
        achievement_status = "Beginner"
    
    achievement_text.text = f'Time\'s up! Achievement: {achievement_status}'  # Menampilkan pencapaian
    timer_text.text = 'Time Left: 0s'  # Mengatur label waktu yang tersisa menjadi 0
    # Menunggu selama 3 detik sebelum memulai simulasi baru
    scene.pause(3)  

# Loop utama untuk menjalankan simulasi berulang kali setelah waktu habis
while True:
    collision_count = 0
    achievement_status = ""
    achievement_text.text = ''
    collision_text.text = 'Collisions: 0'
    vpython_simulation()
