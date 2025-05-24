import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      backgroundColor: const Color(0xFFF2F2F7), // iOS background
      appBar: AppBar(
        backgroundColor: Colors.white,
        title: const Text('groupify',
            style: TextStyle(color: Colors.black, fontWeight: FontWeight.w600)),
        elevation: 0.5,
        actions: const [
          Icon(Icons.qr_code, color: Colors.black87),
          SizedBox(width: 16),
          Icon(Icons.camera_alt, color: Colors.black87),
          SizedBox(width: 16),
          Icon(Icons.more_vert, color: Colors.black87),
          SizedBox(width: 8),
        ],
      ),
      body: Column(
        children: [
          Container(
            color: Colors.white,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: TextField(
              style: const TextStyle(color: Colors.black),
              decoration: InputDecoration(
                filled: true,
                fillColor: const Color(0xFFE5E5EA),
                hintText: 'Search...',
                hintStyle: const TextStyle(color: Colors.black54),
                prefixIcon: const Icon(Icons.search, color: Colors.black45),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide.none,
                ),
                contentPadding: const EdgeInsets.symmetric(vertical: 0),
              ),
            ),
          ),
          const Divider(height: 1),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.only(top: 0),
              itemCount: 12,
              itemBuilder: (context, index) {
                return ListTile(
                  leading: const CircleAvatar(
                    backgroundColor: Color(0xFFD1D1D6), // light gray avatar
                    child: Icon(Icons.person, color: Colors.white),
                  ),
                  title: Text(
                    'Chat Room ${index + 1}',
                    style: const TextStyle(
                        color: Colors.black, fontWeight: FontWeight.w500),
                  ),
                  subtitle: const Text(
                    'Last message preview...',
                    style: TextStyle(color: Colors.black54),
                  ),
                  trailing: const Text('Yesterday',
                      style: TextStyle(color: Colors.black45)),
                  onTap: () {
                    // TODO: navigate to chat screen
                  },
                );
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: const Color(0xFFCC5500), // iOS blue
        onPressed: () {
          // TODO: new chat/group action
        },
        child: const Icon(Icons.chat, color: Colors.white),
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: Colors.white,
        selectedItemColor: Colors.deepOrangeAccent, // iOS blue
        unselectedItemColor: Colors.grey,
        showUnselectedLabels: true,
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.chat), label: 'Chats'),
          BottomNavigationBarItem(icon: Icon(Icons.update), label: 'Updates'),
          BottomNavigationBarItem(
              icon: Icon(Icons.group), label: 'Communities'),
          BottomNavigationBarItem(icon: Icon(Icons.call), label: 'Calls'),
        ],
        onTap: (index) {
          // Optional: handle tab switching
        },
      ),
    );
  }
}
